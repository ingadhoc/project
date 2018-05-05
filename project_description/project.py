##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields


class account_analytic_account(models.Model):
    _inherit = 'account.analytic.account'

    # para simplificar volvemos a crear el mismo campo que ya existia antes
    description = fields.Text(
        'Description',
        help="Account analytic account description"
    )
