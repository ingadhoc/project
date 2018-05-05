##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields


class ProjectTag(models.Model):

    _name = 'project_tags.project_tag'
    _description = 'project_tag'

    name = fields.Char(string='Name', required=True, size=64)
