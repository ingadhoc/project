##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import api, fields, models
from odoo.fields import Domain

CLOSED_STATES = {
    "1_done": "Done",
    "1_canceled": "Canceled",
}


class Task(models.Model):
    _inherit = "project.task"

    @api.model
    def _get_id_prefix_domain(self, prefix):
        enabled_domain = Domain("project_id.show_task_id", "=", True)
        max_task_id = self.search([("project_id.show_task_id", "=", True)], order="id desc", limit=1).id
        if not max_task_id:
            return Domain.FALSE

        prefix_int = int(prefix)
        prefix_domains = [Domain.AND([enabled_domain, Domain("id", "=", prefix_int)])]
        factor = 10
        while prefix_int * factor <= max_task_id:
            prefix_domains.append(
                Domain.AND(
                    [
                        enabled_domain,
                        Domain("id", ">=", prefix_int * factor),
                        Domain("id", "<", (prefix_int + 1) * factor),
                    ]
                )
            )
            factor *= 10
        return Domain.OR(prefix_domains)

    display_in_project = fields.Boolean(default=True)

    @api.depends("project_id")
    def _compute_display_in_project(self):
        """We always want subtasks to be displayed in the project pipeline.
        By default Odoo hides subtasks that share the same project as their
        parent, making them invisible in kanban/list views. We override to
        always set True so every task is visible. Users can still manually
        hide individual tasks using the 'Hide in pipeline' button.
        """
        for task in self:
            task.display_in_project = True

    @api.model_create_multi
    def create(self, vals_list):
        """Force display_in_project=True on creation.
        Odoo's views pass 'default_display_in_project': False in the context
        when creating subtasks, which overrides both the field default and the
        compute. We force it here so subtasks are always visible in the
        pipeline.
        """
        for vals in vals_list:
            vals["display_in_project"] = True
        return super().create(vals_list)

    show_task_id = fields.Boolean(related="project_id.show_task_id", readonly=True)
    dont_send_stage_email = fields.Boolean(
        string="Don't Send Stage Email",
        default=False,
        help="When the task's stage changes, if the stage has an automatic template set, "
        "no email will be send. After the stage changes, this value returns to False so that "
        "new stage changes will send emails.",
    )
    is_closed = fields.Boolean(related="stage_id.fold", string="Folded in Kanban", index=True)

    @api.depends("name", "project_id.show_task_id")
    def _compute_display_name(self):
        super()._compute_display_name()
        for task in self:
            if task.project_id.show_task_id and task.id and task.display_name:
                task.display_name = f"{task.display_name} (#{task.id})"

    @api.model
    def _search_display_name(self, operator, value):
        domain = super()._search_display_name(operator, value)
        normalized_name = (value or "").strip()
        if normalized_name.startswith("#"):
            normalized_name = normalized_name[1:].strip()

        if normalized_name.isdigit() and operator in ("ilike", "like", "=ilike", "=like"):
            return Domain.OR([domain, self._get_id_prefix_domain(normalized_name)])

        return domain

    def _track_template(self, changes):
        task = self[0]
        res = super()._track_template(changes)
        if "stage_id" in changes and task.stage_id.mail_template_id:
            res["stage_id"] = (
                task.stage_id.mail_template_id,
                {
                    "message_type": "comment",
                    "auto_delete_keep_log": False,
                    "subtype_id": self.env["ir.model.data"]._xmlid_to_res_id("mail.mt_comment"),
                    "email_layout_xmlid": "mail.mail_notification_light",
                },
            )
        if "stage_id" in res and task.dont_send_stage_email and task.stage_id.mail_template_id:
            res.pop("stage_id")
            task.dont_send_stage_email = False
        return res

    @api.depends("stage_id", "depend_on_ids.state", "project_id.allow_task_dependencies")
    def _compute_state(self):
        for task in self:
            dependent_open_tasks = []
            if task.allow_task_dependencies:
                dependent_open_tasks = [
                    dependent_task for dependent_task in task.depend_on_ids if dependent_task.state not in CLOSED_STATES
                ]
            # if one of the blocking task is in a blocking state
            if dependent_open_tasks:
                # here we check that the blocked task is not already in a closed state (if the task is already done we don't put it in waiting state)
                if task.state not in CLOSED_STATES:
                    task.state = "04_waiting_normal"
            # if the task as no blocking dependencies and is in waiting_normal, the task goes back to in progress
            elif task.state not in CLOSED_STATES:
                task.state = "01_in_progress"
            if task.stage_id.task_state:
                task.state = task.stage_id.task_state
                task._inverse_state()
