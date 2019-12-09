# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class ResPartner(models.Model):
    _inherit = "res.partner"


    @api.multi
    def unlink(self):
        for rec in self:
            if self.env.user.delete_res_partner:
                return super(ResPartner, self).unlink()
            else:
                raise ValidationError(_('You try to delete a Partner and not have Permissions. You Can Archivate the partner or contact the administrator and request Permissions.'))