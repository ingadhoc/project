# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields


class project_type(models.Model):

    _name = 'project.type'
    _description = 'Project Type'

    name = fields.Char(
        'Name',
        required=True
    )
    description = fields.Text('Description')


class project(models.Model):

    _inherit = 'project.project'

    type_id = fields.Many2one(
        'project.type',
        'Type',
    )
