##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import fields, models


class product_product(models.Model):
    _inherit = 'product.product'
    project_issue_ids = fields.One2many('project.issue',
                                        'product_id',
                                        string='Issues')
