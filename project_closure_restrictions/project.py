# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api, _
from openerp.exceptions import Warning


class project_project(models.Model):
    _inherit = 'project.project'

    @api.onchange('state')
    def onchange_state(self):
        if self.state == 'close':
            for project in self:
                if project.task_ids:
                    tasks_open = project.env['project.task'].search(
                        [('id', 'in', [x.id for x in project.task_ids]),
                         ('stage_id.fold', '!=', True)])
                    if tasks_open:
                        raise Warning(
                            _("You can not close a project with active task,"
                              " we consider active task the one in stages "
                              "without option 'folded'"))

    @api.multi
    def write(self, vals):
        if vals.get('state') == 'close':
            for project in self:
                if project.task_ids:
                    tasks_open = project.env['project.task'].search(
                        [('id', 'in', [x.id for x in project.task_ids]),
                         ('stage_id.fold', '!=', True)])
                    if tasks_open:
                        raise Warning(
                            _("You can not close a project with active task,"
                              " we consider active task the one in stages "
                              "without option 'folded'"))
        return super(project_project, self).write(vals)
