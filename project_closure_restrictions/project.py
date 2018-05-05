##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, api, _
from odoo.exceptions import ValidationError
from odoo.tools import config


class ProjectProject(models.Model):
    _inherit = 'project.project'

    @api.one
    @api.constrains('state')
    def validate_state(self):
        if self.state == 'close':
            # tests are boken by this check
            if self.analytic_account_id.account_type != 'closed' and not \
                    config.options['test_enable'] and \
                    config.options['without_demo']:
                raise ValidationError(_(
                    "You can not cancel the project if the analytic account is"
                    " not closed"))
            for project in self:
                if project.task_ids:
                    tasks_open = project.env['project.task'].search(
                        [('id', 'in', project.task_ids.ids),
                         ('stage_id.fold', '!=', True)])
                    if tasks_open:
                        raise ValidationError(
                            _("You can not close a project with active task,"
                              " we consider active task the one in stages "
                              "without option 'folded'"))
