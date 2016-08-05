# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models


class project_issue(models.Model):
    _inherit = 'project.issue'

    project_issue_solution_id = fields.Many2one('project.issue.solution',
                                                string='Linked Solution')
    issue_description = fields.Html(string='Issue Description')
    solution_description = fields.Html(string='Solution Description')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
