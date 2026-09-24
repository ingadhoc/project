from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ProjectTask(models.Model):
    _inherit = "project.task"

    allow_stock_picking = fields.Boolean(related="project_id.allow_stock_picking")
    picking_ids = fields.One2many(
        comodel_name="stock.picking",
        inverse_name="task_id",
        string="Transfers",
    )
    picking_count = fields.Integer(compute="_compute_picking_count")
    display_create_picking_button = fields.Boolean(compute="_compute_display_create_picking_button")

    @api.depends("picking_ids")
    def _compute_picking_count(self):
        picking_data = self.env["stock.picking"]._read_group([("task_id", "in", self.ids)], ["task_id"], ["__count"])
        counts = {task.id: count for task, count in picking_data}
        for task in self:
            task.picking_count = counts.get(task.id, 0)

    @api.depends("project_id.allow_stock_picking", "project_id.picking_stage_ids", "stage_id")
    def _compute_display_create_picking_button(self):
        for task in self:
            allowed_stages = task.project_id.picking_stage_ids
            task.display_create_picking_button = bool(
                task.project_id.allow_stock_picking and (not allowed_stages or task.stage_id in allowed_stages)
            )

    def _get_stock_picking_context(self):
        self.ensure_one()
        context = {
            "default_task_id": self.id,
            "default_project_id": self.project_id.id,
            "default_partner_id": self.partner_id.id,
            "default_company_id": self.company_id.id or self.env.company.id,
            "default_origin": self.display_name,
        }
        picking_type = self.project_id.picking_type_id
        if picking_type:
            context["default_picking_type_id"] = picking_type.id
        return context

    def action_create_stock_picking(self):
        self.ensure_one()
        if not self.project_id.allow_stock_picking:
            raise UserError(
                _(
                    "Project '%s' does not have transfer management enabled.",
                    self.project_id.display_name,
                )
            )
        if not self.display_create_picking_button:
            raise UserError(
                _(
                    "Stage '%(stage)s' does not allow creating pickings on project '%(project)s'.",
                    stage=self.stage_id.display_name,
                    project=self.project_id.display_name,
                )
            )
        return {
            "type": "ir.actions.act_window",
            "name": _("New Transfer"),
            "res_model": "stock.picking",
            "view_mode": "form",
            "views": [(self.env.ref("stock.view_picking_form").id, "form")],
            "target": "current",
            "context": self._get_stock_picking_context(),
        }

    def action_view_stock_pickings(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("stock.action_picking_tree_all")
        action.update(
            {
                "name": _("Transfers"),
                "domain": [("task_id", "=", self.id)],
                "context": self._get_stock_picking_context(),
            }
        )
        if self.picking_count == 1:
            action["views"] = [(self.env.ref("stock.view_picking_form").id, "form")]
            action["res_id"] = self.picking_ids[0].id
        return action
