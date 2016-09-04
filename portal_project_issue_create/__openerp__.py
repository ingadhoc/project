# -*- coding: utf-8 -*-
##############################################################################
#
#    Sistemas ADHOC - ADHOC SA
#    https://launchpad.net/~sistemas-adhoc
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Portal Project Issue Create',
    'version': '8.0.0.1.0',
    'category': 'Projects & Services',
    'sequence': 14,
    'summary': '',
    'description': """
Portal Project Issue Create
===========================

    """,
    'author': 'ADHOC SA',
    'website': 'www.adhoc.com.ar',
    'images': [
    ],
    'depends': [
        'portal_project_issue',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/portal_security.xml',
        'project_issue_view.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
