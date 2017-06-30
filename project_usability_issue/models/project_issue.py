# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp.osv import fields, osv
from datetime import datetime, timedelta


class ProjectIssue(osv.osv):
    _inherit = 'project.issue'

    def _compute_day(self, cr, uid, ids, fields, args, context=None):
        res = super(ProjectIssue, self)._compute_day(
            cr, uid, ids, fields=fields, args=args, context=context)
        return res

    def _search_days(self, cr, uid, obj, name, args, context):
        new_args = []
        for arg in args:
            field, operator, value = arg
            if field == 'days_since_creation':
                if operator in ('>', '>=', '='):
                    if operator == '>':
                        value += 1
                    new_operator = '<='
                elif operator in ('<', '<='):
                    if operator == '<=':
                        value += 1
                    new_operator = '>='
                else:
                    raise Warning('Operator %s not implemented' % operator)
                if operator == '=':
                    to_date = datetime.today() - timedelta(days=value + 1)
                    new_args += ['&', (
                        'create_date',
                        '>=',
                        to_date.strftime("%Y-%m-%d %H:%M:%S"))]
                date_create = datetime.today() - timedelta(days=value)
                new_arg = (
                    'create_date',
                    new_operator,
                    date_create.strftime("%Y-%m-%d %H:%M:%S"))

                new_args.append(new_arg)
            else:
                new_args.append(arg)
        return new_args

    _columns = {
        'days_since_creation': fields.function(_compute_day,
                                               fnct_search=_search_days,
                                               multi='compute_day',
                                               )
    }
