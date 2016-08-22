# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api


class project_issue(models.Model):
    _inherit = 'project.issue'

    @api.multi
    def message_subscribe(self, partner_ids, subtype_ids=None, context=None):
        res = super(project_issue, self.sudo()).message_subscribe(
            partner_ids, subtype_ids=subtype_ids, context=context)
        return res
