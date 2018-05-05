##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

from odoo import fields, models


class project_issue(models.Model):
    _inherit = 'project.issue'
    _order = "priority desc, sequence, date_deadline, " \
             "duration, create_date desc"

    sequence = fields.Integer('Sequence',
                              index=True,
                              default=10,
                              help="Gives the sequence order when "
                                   "displaying a list of tasks.")
