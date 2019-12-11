# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from ast import literal_eval

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    
    different_name=fields.Boolean('Name',help='Different Name')
    different_estado_padron=fields.Boolean('Estado Padron',help='Different Padron')
    different_state_id=fields.Boolean('State',help='Different State')
    different_street=fields.Boolean('Street',help='Different Street')
    different_empleador_padron=fields.Boolean('Empleador Padron',help='Different Empleador Padron')
    different_imp_ganancias_padron=fields.Boolean('Impuesto Ganancia Padron',help='Different Impuesto Ganancia Padron')
    different_imp_iva_padron=fields.Boolean('Impuesto Iva Padron',help='Different Impuesto Iva Padron')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        
        res.update(
            different_name=bool(ICPSudo.get_param('partner_syncro_afipws.different_name') or False),
            different_estado_padron=bool(ICPSudo.get_param('partner_syncro_afipws.different_estado_padron') or False),
            different_state_id=bool(ICPSudo.get_param('partner_syncro_afipws.different_state_id') or False),
            different_street=bool(ICPSudo.get_param('partner_syncro_afipws.different_street') or False),
            different_empleador_padron=bool(ICPSudo.get_param('partner_syncro_afipws.different_empleador_padron') or False),
            different_imp_ganancias_padron=bool(ICPSudo.get_param('partner_syncro_afipws.different_imp_ganancias_padron') or False),
            different_imp_iva_padron=bool(ICPSudo.get_param('partner_syncro_afipws.different_imp_iva_padron') or False),
        )
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        ICPSudo.set_param("partner_syncro_afipws.different_name", self.different_name)
        ICPSudo.set_param("partner_syncro_afipws.different_estado_padron", self.different_estado_padron)
        ICPSudo.set_param("partner_syncro_afipws.different_state_id", self.different_state_id)
        ICPSudo.set_param("partner_syncro_afipws.different_street", self.different_street)
        ICPSudo.set_param("partner_syncro_afipws.different_different_empleador_padron", self.different_empleador_padron)
        ICPSudo.set_param("partner_syncro_afipws.different_imp_ganancias_padron", self.different_imp_ganancias_padron)
        ICPSudo.set_param("partner_syncro_afipws.different_imp_iva_padron", self.different_imp_iva_padron)