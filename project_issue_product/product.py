# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models


class product_product(models.Model):
    _inherit = 'product.product'
    project_issue_ids = fields.One2many('project.issue',
                                        'product_id',
                                        string='Issues')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
