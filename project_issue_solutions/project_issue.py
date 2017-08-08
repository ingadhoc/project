# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models, api, _
from openerp.tools import html2plaintext
from openerp.exceptions import UserError


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

    @api.multi
    @api.constrains('stage_id')
    def change_stage_id(self):
        for rec in self:
            if rec.stage_id.solution_required:
                if len(html2plaintext(rec.solution_description)) <= 1:
                    raise UserError(_(
                        'You need to complete solution'
                        ' description to change the stage'))
