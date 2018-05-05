##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api


class project(models.Model):
    _inherit = 'project.task'

    task_count_delegate = fields.Integer(
        compute="_compute_task_count",
        store=True,
        string="# Parent Task")

    @api.one
    @api.depends('parent_ids')
    def _compute_task_count(self):
        self.task_count_delegate = len(self.parent_ids)
