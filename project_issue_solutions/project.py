# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models


class task(models.Model):
    _inherit = 'project.task'

    members = fields.Many2many('res.users',
                               'task_user_rel',
                               'task_id', 'uid',
                               string='Task Members',
                               help="Task's members are users who "
                                    "can edit some fields on this task.",
                               states={'done': [('readonly', True)],
                                       'cancelled': [('readonly', True)]})


# class project_work(models.Model):
#     _inherit = "project.task.work"
#
#     @api.multi
#     def write(self, vals):
#         """
#         We change the user id so that it doenst gives error
#         """
#         self._uid = 1
#         return super(project_work, self).write(vals)
