from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProjectProject(models.Model):
    _inherit = "project.project"

    allow_stock_picking = fields.Boolean(
        string="Transfer Management",
        help="Enables, on the tasks of this project, the button to create stock "
        "pickings and the counter of the ones already created.",
    )
    picking_type_id = fields.Many2one(
        comodel_name="stock.picking.type",
        string="Default Operation Type",
        help="If set, the pickings created from the tasks of this project start "
        "with this operation type. If empty, the user chooses it every time.",
    )
    picking_stage_ids = fields.Many2many(
        comodel_name="project.task.type",
        relation="project_project_picking_stage_rel",
        column1="project_id",
        column2="stage_id",
        string="Stages That Allow Transfers",
        help="Task stages on which pickings can be created. If empty, they can be " "created on any stage.",
    )

    @api.constrains("company_id", "picking_type_id")
    def _check_picking_type_company(self):
        for project in self:
            picking_company = project.picking_type_id.company_id
            if picking_company and project.company_id and picking_company != project.company_id:
                raise ValidationError(
                    _(
                        "Operation type '%(picking_type)s' belongs to company "
                        "'%(picking_company)s' and project '%(project)s' belongs to "
                        "'%(project_company)s'.",
                        picking_type=project.picking_type_id.display_name,
                        picking_company=picking_company.display_name,
                        project=project.display_name,
                        project_company=project.company_id.display_name,
                    )
                )
