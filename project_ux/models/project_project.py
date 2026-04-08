##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    show_task_id = fields.Boolean(
        string="Show Task ID",
    )
