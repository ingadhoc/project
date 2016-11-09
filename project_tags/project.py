# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields


class project(models.Model):
    _inherit = 'project.project'

    project_tag_ids = fields.Many2many(
        'project.tags',
        'project_project_tag_ids_rel',
        'project_id',
        'project_tag_id',
        string='Tags')
