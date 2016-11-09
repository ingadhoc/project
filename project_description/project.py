# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields


class account_analytic_account(models.Model):
    _inherit = 'account.analytic.account'

    # para simplificar volvemos a crear el mismo campo que ya existia antes
    description = fields.Text(
        'Description',
        help="Account analytic account description"
    )
