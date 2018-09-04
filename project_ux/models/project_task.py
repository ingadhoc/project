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

    @api.onchange('template_task_id')
    def onchange_template(self):
        if not self.template_task_id:
            return
        copy_data_default = {
            'project_id': self.project_id.id,
            'partner_id': self.partner_id.id,
            'company_id': self.company_id.id,
            'message_last_post': False,
            'child_ids': False,
        }
        data = self.template_task_id.copy_data(copy_data_default)
        for k, v in data[0].items():
            self[k] = v

        childs = []
        copy_data_default['project_id'] = self.subtask_project_id.id
        for child in self.template_task_id.child_ids:
            childs.append((0, 0, child.copy_data(copy_data_default)[0]))
        self.child_ids = childs

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

    @api.constrains('project_id')
    def change_project_id(self):
        for rec in self.filtered('child_ids'):
            rec.child_ids.update(
                {'project_id': rec.subtask_project_id.id,
                 })
