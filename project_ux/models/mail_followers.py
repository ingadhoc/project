from odoo import models
from odoo.tools.sql import create_index


class MailFollowers(models.Model):
    _inherit = "mail.followers"

    def init(self):
        super().init()
        create_index(  # used by the project.task record rules on followers
            self.env.cr,
            indexname="mail_followers_project_task_partner_id_res_id_index",
            tablename=self._table,
            expressions=["partner_id", "res_id"],
            where="res_model = 'project.task'",
        )
