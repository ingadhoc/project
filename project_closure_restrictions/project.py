# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api, _
from openerp.exceptions import ValidationError


class ProjectProject(models.Model):
    _inherit = 'project.project'

    @api.one
    @api.constrains('state')
    def validate_state(self):
        if self.state == 'close':
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
