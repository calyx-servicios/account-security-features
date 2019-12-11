# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields, _

import zipfile
import csv
import urllib.request 
import datetime
import logging
from datetime import date

_logger = logging.getLogger(__name__)

from openerp.tools import DEFAULT_SERVER_DATE_FORMAT


class ResPartnerSyncroAfip(models.Model):
    _name = "res.partner.syncro"


    @api.multi
    def action_partner_cron_syncro(self):
        self.action_partner_cron_syncro_afipws()
    
    @api.multi
    def action_partner_cron_syncro_afipws(self):
        _logger.debug('======>action_partner_cron_syncro_afipws<======')
        count=0
        filters = self.env['res.partner'].get_filters()
        if len(filters)>0:
            for partner in self.env['res.partner'].search([('supplier', '=', True)]):
                try:
                    changes=partner.check_changes_partner(filters)
                    #changes=True
                    _logger.debug('=====partner:%r ===>%r' % (partner.name,changes))
                    if changes:
                        count+=1
                except:
                    pass
            if count>0:
                self.alert_syncro_change(count)
        #alert if no filter is configured
    
    @api.multi
    def alert_syncro_change(self, count):
        _logger.debug('======>alert_afip_change<======')
        subject='Partner Afip Different Data '
        message='('+str(count)+') Differences Found from Afip WS Data'

        user_ids=self.env['res.users'].search([('active','=',True)])
        self.env['mail.message'].create({'message_type':'notification',
                'body': message,
                'subject': subject,
                'needaction_partner_ids': [(4, user.partner_id.id, None) for user in user_ids], 
                })

    


    

class ResPartner(models.Model):
    _inherit = "res.partner"
    different = fields.Boolean(string='Afip Different',default=False,track_visibility='onchange')
    
    
    @api.model
    def _get_default_title_case(self):
        parameter = self.env['ir.config_parameter'].sudo().get_param(
            'use_title_case_on_padron_afip')
        if parameter == 'False' or parameter == '0':
            return False
        return True

    

    @api.multi
    def check_changes_partner(self, filters=None):
        self.ensure_one()
        title_case=self._get_default_title_case()
        if not filters:
            filters=[]

        partner_vals = self.get_data_from_padron_afip()
        lines = []
        _logger.debug('=====partner_vals=====%r',partner_vals)
        _logger.debug('=====partner_vfilters====%r',filters)
        # partner_vals.pop('constancia')
        for key, new_value in partner_vals.items():
            old_value = self[key]
            if new_value == '':
                new_value = False
            if title_case and key in ('name', 'city', 'street'):
                new_value = new_value and new_value.title()
            if key in ('impuestos_padron', 'actividades_padron'):
                old_value = old_value.ids
            elif key in ('state_id', 'afip_responsability_type_id'):
                old_value = old_value.id
            if new_value  and \
                    old_value != new_value and key in filters:
                line_vals = {
                    'field': key,
                    'old_value': old_value,
                    # 'new_value': new_value,
                    'new_value': new_value or False,
                }
                lines.append(line_vals)
        if len(lines)>0:
            self.different=True
        return self.different

    @api.multi
    def action_partner_check_syncro(self):
        different=False
        filters=self.get_filters()
        try:
            different=self.check_changes_partner(filters)
        except:
            pass
        self.different=different

    @api.multi
    def get_filters(self):
        ICPSudo = self.env['ir.config_parameter'].sudo()
        different_name=bool(ICPSudo.get_param('partner_syncro_afipws.different_name') or False)
        different_estado_padron=bool(ICPSudo.get_param('partner_syncro_afipws.different_estado_padron') or False)
        different_state_id=bool(ICPSudo.get_param('partner_syncro_afipws.different_state_id') or False)
        different_street=bool(ICPSudo.get_param('partner_syncro_afipws.different_street') or False)
        different_empleador_padron=bool(ICPSudo.get_param('partner_syncro_afipws.different_empleador_padron') or False)
        different_imp_ganancias_padron=bool(ICPSudo.get_param('partner_syncro_afipws.different_imp_ganancias_padron') or False)
        different_imp_iva_padron=bool(ICPSudo.get_param('partner_syncro_afipws.different_imp_iva_padron') or False)
        filters=[]
        if different_name:
            filters.append('name')
        if different_estado_padron:
            filters.append('estado_padron')
        if different_state_id:
            filters.append('state_id')
        if different_street:
            filters.append('street')
        if different_empleador_padron:
            filters.append('empleador_padron')
        if different_imp_ganancias_padron:
            filters.append('imp_ganancias_padron')
        if different_imp_iva_padron:
            filters.append('imp_iva_padron')
        _logger.debug('======>FILTERS<======')
        _logger.debug('%r',filters)
        return filters

        
        
    


        
