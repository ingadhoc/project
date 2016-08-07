# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################


from openerp import fields, models
from openerp.tools.translate import _


class project_task_type(models.Model):
    _name = 'project.task.phase'
    _description = 'Task Phase'
    _order = 'sequence'
    name = fields.Char(string='Phase Name',
                       required=True,
                       size=64,
                       translate=True)
    sequence = fields.Integer(string='Sequence')


class task(models.Model):
    _inherit = 'project.task'
    phase_id = fields.Many2one('project.task.phase',
                               string='Phase')
