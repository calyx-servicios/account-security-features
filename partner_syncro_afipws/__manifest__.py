##############################################################################
#
#    Copyright (C) 2019  Calyx  (http://www.calyxservicios.com.ar)
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
    'name': 'Partner Syncro AFIP Web Service',
    'version': '11.0.1.0.0',
    'category': 'Tools',
    'author': "Calyx",
    'website': 'www.calyxservicios.com.ar',
    'license': 'AGPL-3',
    'summary': '''Partner Syncro AFIP Web Service.''',
    'depends': [
        'base','l10n_ar_account','l10n_ar_partner'
    ],
    'external_dependencies': {
    },
    'data': [
        'view/res_partner_view.xml',
        'data/cron.xml',
        'view/res_config_settings_views.xml'
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
