# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################


from odoo import models, api


class project(models.Model):

    """"""

    _inherit = 'project.project'

    @api.one
    def copy(self, default=None):
        res = super(project, self).copy(default)
        res.message_ids.unlink()
        res.analytic_account_id.message_ids.unlink()
        return res
