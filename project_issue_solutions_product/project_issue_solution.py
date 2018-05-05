##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import fields, models


class project_isssue_solution(models.Model):
    """ Note """
    _inherit = 'project.issue.solution'

    product_ids = fields.Many2many(
        'product.product',
        'project_issue_solution_product_rel',
        'solution_id',
        'product_id',
        string='Products'
    )
