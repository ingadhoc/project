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
    kanban_state = fields.Selection(
        [('normal', 'In Progress'),
         ('blocked', 'Blocked'),
         ('done', 'Ready for next stage')],
        track_visibility='onchange',
        help="A task's kanban state indicates special "
             "situations affecting it:\n"
        " * Normal is the default situation\n"
        " * Blocked indicates something is preventing "
             "the progress of this task\n"
        " * Ready for next stage indicates the task is ready "
             "to be pulled to the next stage",
        required=False,
        copy=False,
    )
