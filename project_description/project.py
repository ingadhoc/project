# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields


class account_analytic_account(models.Model):
    _inherit = 'account.analytic.account'

    description = fields.Text('Description',
                              help="Account analytic account description")
