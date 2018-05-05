##############################################################################
#
#    Copyright (C) 2015  ADHOC SA  (http://www.adhoc.com.ar)
#    All Rights Reserved.
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
    "name": "Project Task Activity",
    'version': '9.0.1.0.0',
    'category': 'Tools',
    'sequence': 14,
    'author': 'ADHOC SA',
    'website': 'www.adhoc.com.ar',
    'license': 'AGPL-3',
    'summary': '',
    'depends': [
        'project',
    ],
    'external_dependencies': {
    },
    'data': [
        'view/activities_menuitem.xml',
        'view/project_view.xml',
        'view/task_view.xml',
        'security/ir.model.access.csv',
        'security/project_security.xml',
    ],
    'demo': [
        'demo/project_task_activity_demo.yml',
        'demo/project_activity_demo.xml',
    ],
    'installable': False,
    'auto_install': False,
    'application': False,
}
