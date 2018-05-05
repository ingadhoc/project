# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from openerp import models, fields


class project(models.Model):
    _inherit = 'project.project'

    project_tag_ids = fields.Many2many(
        'project_tags.project_tag',
        'project_project_tag_ids_rel',
        'project_id',
        'project_tag_id',
        string='Tags')
