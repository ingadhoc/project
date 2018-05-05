##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################


from odoo import fields, models


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
