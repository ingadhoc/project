##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################


import re
from odoo import netsvc
from odoo.osv import osv, fields


class project(osv.osv):
    """"""

    _name = 'project.project'
    _inherits = {}
    _inherit = ['project.project']

    _columns = {
        'related_to_ids': fields.many2many('project.project', 'project_project_related_rel', 'project_id', 'related_to_id', 'Related To Projects'),
        'related_by_ids': fields.many2many('project.project', 'project_project_related_rel', 'related_to_id', 'project_id', 'Related By Projects'),

        #        'parent_ids': fields.many2many('project.project', 'project_project_parent_rel', 'project_id', 'parent_id', 'Parent Projects'),
        #        'child_ids': fields.many2many('project.project', 'project_project_parent_rel', 'parent_id', 'project_id', 'Delegated Project'),
        #        'realated_project_ids': fields.many2many('project.project', 'project_related_projects_realated_project_ids_project_related_ids_rel', 'project_id', 'project_id', string='Related Project'),
    }

    _defaults = {
    }

    _constraints = [
    ]


project()
