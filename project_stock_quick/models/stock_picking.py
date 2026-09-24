from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    task_id = fields.Many2one(
        comodel_name="project.task",
        string="Task",
        index="btree_not_null",
        check_company=True,
        help="Task this picking was created from.",
    )

    @api.onchange("task_id")
    def _onchange_task_id(self):
        """Keep project and contact aligned with the task chosen by hand."""
        for picking in self.filtered("task_id"):
            picking.project_id = picking.task_id.project_id
            if picking.task_id.partner_id:
                picking.partner_id = picking.task_id.partner_id
