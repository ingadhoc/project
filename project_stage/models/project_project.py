##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields


class ProjectProject(models.Model):

    _inherit = 'project.project'
    _order = "sequence"

    stage_id = fields.Many2one(
        'project.stage',
        'Stage',
        track_visibility='onchange',
        index=True,
        copy=False,
    )
