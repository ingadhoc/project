##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields


class Task(models.Model):
    _inherit = 'project.task'

    dont_send_stage_email = fields.Boolean(
        string="Don't Send Stage Email",
        default=False,
        help="When the task's stage changes, if the stage has an automatic template set, "
        "no email will be send. After the stage changes, this value returns to False so that "
        "new stage changes will send emails."
    )

    def _track_template(self, changes):
        task = self[0]
        res = super()._track_template(changes)
        if 'stage_id' in changes and task.stage_id.mail_template_id:
            res['stage_id'] = (task.stage_id.mail_template_id, {
                'message_type': 'comment',
                'auto_delete_message': True,
                'email_layout_xmlid': 'mail.mail_notification_light'})
        if 'stage_id' in res and task.dont_send_stage_email and task.stage_id.mail_template_id:
            res.pop('stage_id')
            task.dont_send_stage_email = False
        return res
