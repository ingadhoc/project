# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models, api


class ProjectIsssueSolution(models.Model):

    """ Note """
    _name = 'project.issue.solution'
    _inherit = ['mail.thread']
    _description = "Project Issue Solution"
    _order = 'name'

    name = fields.Char(
        string='Name',
        required=True
    )
    solution_description = fields.Html(
        string='Solution Description'
    )
    issue_description = fields.Html(
        string='Issue Description'
    )
    tags_ids = fields.Many2many(
        'project.solution.tag',
        string='Tags'
    )
    project_issue_ids = fields.One2many(
        'project.issue',
        'project_issue_solution_id',
        string='Issues',
    )
    issue_count = fields.Integer(
        compute='_compute_issue_count'
    )

    @api.multi
    @api.depends('project_issue_ids')
    def _compute_issue_count(self):
        for rec in self:
            rec.issue_count = len(rec.project_issue_ids)
