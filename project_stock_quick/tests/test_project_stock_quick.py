from odoo.exceptions import UserError, ValidationError
from odoo.tests import Form, TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestProjectStockQuick(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Test Customer"})
        cls.project = cls.env["project.project"].create(
            {
                "name": "Project With Transfers",
                "partner_id": cls.partner.id,
                "allow_stock_picking": True,
            }
        )
        cls.task = cls.env["project.task"].create(
            {
                "name": "Task With Transfers",
                "project_id": cls.project.id,
                "partner_id": cls.partner.id,
            }
        )
        cls.stage_todo = cls.env["project.task.type"].create(
            {
                "name": "To Do",
                "sequence": 1,
                "project_ids": [(4, cls.project.id)],
            }
        )
        cls.stage_done = cls.env["project.task.type"].create(
            {
                "name": "Terminada",
                "sequence": 2,
                "project_ids": [(4, cls.project.id)],
            }
        )
        cls.picking_type = cls.env["stock.picking.type"].search(
            [
                ("code", "=", "outgoing"),
                ("company_id", "in", [cls.env.company.id, False]),
            ],
            limit=1,
        )

    def _create_picking(self, task=None):
        return self.env["stock.picking"].create(
            {
                "picking_type_id": self.picking_type.id,
                "partner_id": self.partner.id,
                "project_id": self.project.id,
                "task_id": (task or self.task).id,
            }
        )

    def test_allow_stock_picking_follows_project(self):
        self.assertTrue(self.task.allow_stock_picking)
        self.project.allow_stock_picking = False
        self.assertFalse(self.task.allow_stock_picking)

    def test_create_action_carries_task_defaults(self):
        action = self.task.action_create_stock_picking()
        self.assertEqual(action["res_model"], "stock.picking")
        self.assertEqual(action["view_mode"], "form")
        context = action["context"]
        self.assertEqual(context["default_task_id"], self.task.id)
        self.assertEqual(context["default_project_id"], self.project.id)
        self.assertEqual(context["default_partner_id"], self.partner.id)

    def test_picking_count_and_view_action(self):
        self.assertEqual(self.task.picking_count, 0)

        picking = self._create_picking()
        self.task.invalidate_recordset(["picking_ids", "picking_count"])
        self.assertEqual(self.task.picking_count, 1)

        # a single picking opens straight in its form
        action = self.task.action_view_stock_pickings()
        self.assertEqual(action["res_id"], picking.id)
        self.assertEqual(action["domain"], [("task_id", "=", self.task.id)])

        self._create_picking()
        self.task.invalidate_recordset(["picking_ids", "picking_count"])
        self.assertEqual(self.task.picking_count, 2)
        # _for_xml_id always carries res_id, so an empty one means "open the list"
        self.assertFalse(self.task.action_view_stock_pickings().get("res_id"))

    def test_picking_count_ignores_other_tasks(self):
        other_task = self.env["project.task"].create(
            {
                "name": "Another Task",
                "project_id": self.project.id,
            }
        )
        self._create_picking()
        self.assertEqual(other_task.picking_count, 0)

    def test_onchange_task_fills_project_and_partner(self):
        with Form(self.env["stock.picking"].with_context(default_picking_type_id=self.picking_type.id)) as picking_form:
            picking_form.task_id = self.task
            self.assertEqual(picking_form.project_id, self.project)
            self.assertEqual(picking_form.partner_id, self.partner)

    def test_default_picking_type_only_when_configured(self):
        self.assertNotIn("default_picking_type_id", self.task._get_stock_picking_context())

        self.project.picking_type_id = self.picking_type
        self.assertEqual(
            self.task._get_stock_picking_context()["default_picking_type_id"],
            self.picking_type.id,
        )

    def test_no_stages_configured_allows_any_stage(self):
        self.assertFalse(self.project.picking_stage_ids)
        for stage in self.stage_todo | self.stage_done:
            self.task.stage_id = stage
            self.assertTrue(self.task.display_create_picking_button)

    def test_stages_configured_gate_the_button(self):
        self.project.picking_stage_ids = self.stage_todo

        self.task.stage_id = self.stage_todo
        self.assertTrue(self.task.display_create_picking_button)

        self.task.stage_id = self.stage_done
        self.assertFalse(self.task.display_create_picking_button)

    def test_action_refuses_a_stage_that_is_not_allowed(self):
        self.project.picking_stage_ids = self.stage_todo
        self.task.stage_id = self.stage_done
        with self.assertRaises(UserError):
            self.task.action_create_stock_picking()

    def test_action_refuses_a_project_without_the_feature(self):
        self.project.allow_stock_picking = False
        with self.assertRaises(UserError):
            self.task.action_create_stock_picking()

    def test_picking_type_of_another_company_is_rejected(self):
        other_company = self.env["res.company"].create({"name": "Another Company"})
        other_picking_type = self.env["stock.picking.type"].search([("company_id", "=", other_company.id)], limit=1)
        self.assertTrue(other_picking_type, "the new company should come with its own operation types")
        self.project.company_id = self.env.company
        with self.assertRaises(ValidationError):
            self.project.picking_type_id = other_picking_type
