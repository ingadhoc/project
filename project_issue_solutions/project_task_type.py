# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    solution_required = fields.Boolean(
        string="Solution Required?",
        help='If you set it to true, then issues that moves into this stage '
        'will require a solution.'
    )
