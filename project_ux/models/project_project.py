##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields


class ProjectProject(models.Model):
    _name = 'project.project'
    _inherit = ['project.project', 'mail.activity.mixin']

    sub_task_count = fields.Integer(
        compute='_compute_sub_task_count',
    )

    def _compute_sub_task_count(self):
        task_data = self.env['project.task'].read_group([
            ('parent_id', '!=', False),
            ('project_id', 'in', self.ids),
            '|', ('stage_id.fold', '=', False),
            ('stage_id', '=', False)], ['project_id'], ['project_id'])
        result = dict(
            (data['project_id'][0],
             data['project_id_count']) for data in task_data)
        for project in self:
            project.update({'sub_task_count': result.get(project.id, 0)})

    # We rewrite the method because it is not very heritable,
    # and we need to count only the tasks, not the subtasks
    def _compute_task_count(self):
        task_data = self.env['project.task'].read_group([
            ('parent_id', '=', False),
            ('project_id', 'in', self.ids), '|', (
                'stage_id.fold', '=', False),
            ('stage_id', '=', False)], ['project_id'], ['project_id'])
        result = dict((data['project_id'][0], data['project_id_count'])
                      for data in task_data)
        for project in self:
            project.update({'task_count': result.get(project.id, 0)})
