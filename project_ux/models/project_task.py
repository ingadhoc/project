##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, api, fields


class ProjectTask(models.Model):
    _inherit = 'project.task'

    template_task = fields.Boolean(
        copy=False,
    )

    template_task_id = fields.Many2one(
        'project.task',
        compute="_compute_template_task_id",
        domain=[('template_task', '=', True)],
        string='Template Task',
        copy=False,
        readonly=False,
    )

    @api.multi
    def _compute_template_task_id(self):
        return None

    @api.onchange('template_task_id')
    def onchange_template(self):
        if not self.template_task_id:
            return
        data = self.template_task_id.copy_data()
        for k, v in data[0].items():
            if k in ['project_id', 'partner_id',
                     'company_id', 'message_last_post']:
                continue
            self.update({k: v})
