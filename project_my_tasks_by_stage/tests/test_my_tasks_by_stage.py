from lxml import etree
from odoo.tests.common import TransactionCase
from odoo.tools.safe_eval import safe_eval


class TestMyTasksByStage(TransactionCase):
    def setUp(self):
        super().setUp()
        self.action = self.env.ref("project.action_view_my_task")
        self.context = safe_eval(self.action.context, {"uid": self.env.uid})

    def _default_group_by(self, view_mode):
        view = self.action.view_ids.filtered(lambda v: v.view_mode == view_mode).view_id
        arch = self.env["project.task"].get_view(view.id, view_mode)["arch"]
        return etree.fromstring(arch).get("default_group_by")

    def test_my_tasks_views_group_by_project_stage(self):
        """My Tasks must group by the project task stage, not the personal one."""
        self.assertEqual(self._default_group_by("list"), "stage_id")
        self.assertEqual(self._default_group_by("kanban"), "stage_id")

    def test_action_context_is_not_overridden(self):
        """The context stays with the one of Odoo, so it does not clash with other modules."""
        self.assertNotIn("group_by", self.context)
        self.assertEqual(self.context["search_default_open_tasks"], 1)
        self.assertEqual(self.context["default_user_ids"], [(4, self.env.uid)])

    def test_grouping_by_stage_is_valid_on_tasks(self):
        """The grouping of the views must be accepted by the task model."""
        stage = self.env["project.task.type"].create({"name": "Stage"})
        project = self.env["project.project"].create({"name": "Project", "type_ids": [(6, 0, stage.ids)]})
        self.env["project.task"].create(
            {
                "name": "Task",
                "project_id": project.id,
                "stage_id": stage.id,
                "user_ids": [(4, self.env.uid)],
            }
        )
        groups = self.env["project.task"]._read_group(
            [("user_ids", "in", self.env.uid)],
            groupby=[self._default_group_by("list")],
            aggregates=["__count"],
        )
        self.assertIn(stage, [group[0] for group in groups])
