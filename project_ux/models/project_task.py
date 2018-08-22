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
    child_ids = fields.One2many(
        copy=True,
    )

    @api.multi
    def _compute_template_task_id(self):
        return None

    @api.multi
    def copy_data(self, default=None):
        if default is None:
            default = {}
        res = super(ProjectTask, self).copy_data(default)
        if self._context.get('onchange_template'):
            for rec in res:
                for item in list(rec):
                    if item in [
                            'project_id', 'partner_id',
                            'company_id', 'message_last_post']:
                        rec.pop(item)
        return res

    @api.onchange('template_task_id')
    def onchange_template(self):
        if not self.template_task_id:
            return
        data = self.template_task_id.with_context(
            onchange_template=True).copy_data()
        for k, v in data[0].items():
            self[k] = v

    # We overwrite this function because it is not possible to inherit it and
    # we do that calculates only the subtasks that are in the closed stages.
    @api.multi
    def _compute_subtask_count(self):
        for task in self:
            task.subtask_count = self.search_count(
                [('id', 'child_of', task.id),
                 ('id', '!=', task.id),
                 '|', ('stage_id.fold', '=', False),
                 ('stage_id', '=', False)])

    def action_subtask(self):
        action = super(ProjectTask, self).action_subtask()
        if action.get('context', {}).get('search_default_is_task', False):
            action.get('context').pop('search_default_is_task')
        return action
