##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models


class project_task(models.Model):
    _inherit = 'project.task'
    _order = "priority desc, sequence, " \
             "date_deadline, planned_hours, " \
             "date_start, create_date desc"
