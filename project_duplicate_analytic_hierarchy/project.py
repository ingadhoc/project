# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api


class ProjectProject(models.Model):
    _inherit = 'project.project'

    @api.one
    def copy(self, default=None):
        return super(ProjectProject, self.with_context(
            analytic_project_copy=False)).copy(default=default)
