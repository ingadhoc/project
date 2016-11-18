# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models


class ProjectIssue(models.Model):
    _inherit = 'project.issue'

    project_issue_solution_id = fields.Many2one(
        'project.issue.solution',
        string='Linked Solution'
    )
    issue_description = fields.Html(
        string='Issue Description'
    )
    solution_description = fields.Html(
        string='Solution Description'
    )
