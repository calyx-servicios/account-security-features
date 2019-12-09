##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class ResUsers(models.Model):
    _inherit = "res.users"

    delete_res_partner = fields.Boolean(string='Can Delete a Partner?')