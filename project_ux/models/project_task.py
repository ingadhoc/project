##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api

CLOSED_STATES = {
    '1_done': 'Done',
    '1_canceled': 'Canceled',
}

class Task(models.Model):
    _inherit = 'project.task'

    dont_send_stage_email = fields.Boolean(
        string="Don't Send Stage Email",
        default=False,
        help="When the task's stage changes, if the stage has an automatic template set, "
        "no email will be send. After the stage changes, this value returns to False so that "
        "new stage changes will send emails."
    )
    is_closed = fields.Boolean(related="stage_id.fold", string="Folded in Kanban", store=True, index=True)

    def _track_template(self, changes):
        task = self[0]
        res = super()._track_template(changes)
        if 'stage_id' in changes and task.stage_id.mail_template_id:
            res['stage_id'] = (task.stage_id.mail_template_id, {
                'message_type': 'comment',
                'auto_delete_keep_log': False,
                'email_layout_xmlid': 'mail.mail_notification_light'})
        if 'stage_id' in res and task.dont_send_stage_email and task.stage_id.mail_template_id:
            res.pop('stage_id')
            task.dont_send_stage_email = False
        return res

    @api.depends('stage_id', 'depend_on_ids.state', 'project_id.allow_task_dependencies')
    def _compute_state(self):
        for task in self:
            dependent_open_tasks = []
            if task.allow_task_dependencies:
                dependent_open_tasks = [dependent_task for dependent_task in task.depend_on_ids if dependent_task.state not in CLOSED_STATES]
            # if one of the blocking task is in a blocking state
            if dependent_open_tasks:
                # here we check that the blocked task is not already in a closed state (if the task is already done we don't put it in waiting state)
                if task.state not in CLOSED_STATES:
                    task.state = '04_waiting_normal'
            # if the task as no blocking dependencies and is in waiting_normal, the task goes back to in progress
            elif task.state not in CLOSED_STATES:
                task.state = '01_in_progress'
            if task.stage_id.task_state:
                task.state = task.stage_id.task_state
