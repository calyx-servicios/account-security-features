from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval


class ResPartnerIdNumber(models.Model):

    _inherit = "res.partner"

    constancia_cuit = fields.Binary(string="C.U.I.T")
    estatuto_social = fields.Binary(string="Estatuto social")
    acta_directorio = fields.Binary(string="Acta Directorio")
    constancia_cbu = fields.Binary(string="CBU")