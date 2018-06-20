##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    # para simplificar volvemos a crear el mismo campo que ya existia antes
    description = fields.Text(
        help="Description of the project",
    )
