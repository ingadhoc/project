# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api


class project(models.Model):
    _inherit = 'project.task'

    task_count_delegate = fields.Integer(
        compute="_compute_task_count",
        store=True,
        string="Task Delegate")

    @api.one
    @api.depends('parent_ids')
    def _compute_task_count(self):
        self.task_count_delegate = len(self.parent_ids)
