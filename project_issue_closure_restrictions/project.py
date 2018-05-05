# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, api, _
from odoo.exceptions import ValidationError


class ProjectProject(models.Model):
    _inherit = 'project.project'

    @api.one
    @api.constrains('state')
    def validate_state_from_issues(self):
        if self.state == 'close':
            for project in self:
                if project.issue_ids:
                    issues_open = project.env['project.issue'].search(
                        [('id', 'in', project.issue_ids.ids),
                         ('stage_id.fold', '!=', True)])
                    if issues_open:
                        raise ValidationError(
                            _("You can not close a project with active issues,"
                              " we consider active issue the one in stages "
                              "without option 'folded'"))


class ProjectIssue(models.Model):
    _inherit = 'project.issue'

    @api.one
    @api.constrains('stage_id')
    def validate_issue(self):
        if self.task_id and self.stage_id.closed:
            task_open = self.env['project.task'].search(
                [('id', '=', self.task_id.id),
                 ('stage_id.closed', '!=', True)])
            if task_open:
                raise ValidationError(_(
                    "You can not close an issue with active task, we consider"
                    " active task the one in stages without option 'closed'"))
