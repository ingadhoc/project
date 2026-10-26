##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import api, fields, models
from odoo.fields import Domain


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

    @api.depends("name", "project_id.show_task_id")
    def _compute_display_name(self):
        super()._compute_display_name()
        for task in self:
            if task.project_id.show_task_id and task.id and task.display_name:
                task.display_name = f"{task.display_name} (#{task.id})"

    def onchange(self, values, field_names, fields_spec):
        result = super().onchange(values, field_names, fields_spec)
        # In the quick-create (My Tasks, project kanban) the "Task Title" input
        # is bound to display_name and is only inversed into `name` on save.
        # Because this module makes display_name depend on project_id (to append
        # the task id), changing the project recomputes display_name from the
        # still-empty `name`, blanking the title the user just typed. Restore the
        # typed value in the onchange result so it survives the project change.
        typed_title = values.get("display_name")
        if (
            "project_id" in (field_names or [])
            and typed_title
            and not values.get("name")
            and not result.get("value", {}).get("display_name")
        ):
            result.setdefault("value", {})["display_name"] = typed_title
        return result

    @api.model
    def _search_display_name(self, operator, value):
        domain = super()._search_display_name(operator, value)
        normalized_name = (value or "").strip()
        if normalized_name.startswith("#"):
            normalized_name = normalized_name[1:].strip()

        if normalized_name.isdigit() and operator in ("ilike", "like", "=ilike", "=like"):
            return Domain.OR([domain, self._get_id_prefix_domain(normalized_name)])

        return domain

    def _track_template_parameters(self, tracked_fields):
        task = self[0]
        res = super()._track_template_parameters(tracked_fields)
        if "stage_id" in tracked_fields and task.stage_id.mail_template_id:
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

    # Only the extra dependency is declared: the ORM merges the depends of every
    # _compute_state in the MRO, so the core ones still apply.
    @api.depends("project_id.allow_task_dependencies")
    def _compute_state(self):
        """Let the stage force the task state, on top of the core computation."""
        super()._compute_state()
        for task in self:
            if task.stage_id.task_state:
                task.state = task.stage_id.task_state
                task._inverse_state()
