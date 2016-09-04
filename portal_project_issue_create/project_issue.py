# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api, fields


class project_issue(models.Model):
    _inherit = 'project.issue'

    @api.model
    def _get_default_user(self):
        """
        If portal user is creating issue, then no assigned user
        """
        if self.env.user.has_group('base.group_portal'):
            return False
        return self.env.user.id

    @api.model
    def _get_default_partner(self):
        """
        If portal user is creating issue, then he is the contact
        """
        if self.env.user.has_group('base.group_portal'):
            return self.env.user.partner_id.id
        return super(project_issue, self)._get_default_partner()

    user_id = fields.Many2one(
        default=_get_default_user)
    partner_id = fields.Many2one(
        default=_get_default_partner)

    @api.multi
    def on_change_project(self, project_id):
        """
        If portal user is creating issue, then he is the contact
        """
        if self.env.user.has_group('base.group_portal'):
            partner = self.env.user.partner_id
            return {'value': {
                'partner_id': partner.id,
                'email_from': partner.email}}
        return super(project_issue, self).on_change_project(project_id)

    @api.multi
    def message_subscribe(self, partner_ids, subtype_ids=None, context=None):
        res = super(project_issue, self.sudo()).message_subscribe(
            partner_ids, subtype_ids=subtype_ids, context=context)
        return res
