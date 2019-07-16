##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields


class ProjectProject(models.Model):
    _inherit = 'project.project'

    # para simplificar volvemos a crear el mismo campo que ya existia antes
    description = fields.Text(
        help="Description of the project",
    )
