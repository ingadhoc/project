# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from openerp import fields, models


class project_issue(models.Model):
    _inherit = 'project.issue'
    product_id = fields.Many2one('product.product',
                                 string='Product')
