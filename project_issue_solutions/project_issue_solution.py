# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models


class project_isssue_solution(models.Model):

    """ Note """
    _name = 'project.issue.solution'
    _inherit = ['mail.thread']
    _description = "Project Issue Solution"
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    solution_description = fields.Html(string='Solution Description')
    issue_description = fields.Html(string='Issue Description')
    tags_ids = fields.Many2many('project.tags',
                                string='Tags')
    project_issue_ids = fields.One2many('project.issue',
                                        'project_issue_solution_id',
                                        string='Issues')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
