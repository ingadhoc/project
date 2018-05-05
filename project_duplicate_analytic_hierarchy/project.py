##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, api


class ProjectProject(models.Model):
    _inherit = 'project.project'

    @api.one
    def copy(self, default=None):
        return super(ProjectProject, self.with_context(
            analytic_project_copy=False)).copy(default=default)
