##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields

class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    state_change = fields.Boolean(
        default=False,
        help="When the task's stage changes, if the state change is checked it will change the state of the task into the state selected"
    )

    task_state = fields.Selection(selection=lambda self: self.env['project.task'].fields_get(allfields=['state'])['state']['selection'])
