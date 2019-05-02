##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api


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

    @api.multi
    def copy(self, default=None):
        project = super(ProjectProject, self).copy(default)
        # If we have subtasks we need to fix the project of this substasks
        # manually asigning the new project_id, if not the new subtasks will
        # refer to the template project
        if self.subtask_project_id == self:
            subtasks = self.tasks.filtered(
                lambda t: t.parent_id and t.parent_id.project_id == project)
            subtasks.write({'project_id': project.id})
            project.subtask_project_id = project.id
        return project

    @api.multi
    def map_tasks(self, new_project_id):
        """ copy and map tasks from old to new project """
        tasks = self.env['project.task']
        # We filtered by the tasks only, the subtask will duplicate by the
        # parent
        for task in self.tasks.filtered(lambda x: not x.parent_id):
            # preserve task name and stage, normally altered during copy
            defaults = {'stage_id': task.stage_id.id,
                        'name': task.name}
            tasks += task.copy(defaults)
        return self.browse(new_project_id).write(
            {'tasks': [(6, 0, tasks.ids)]})
