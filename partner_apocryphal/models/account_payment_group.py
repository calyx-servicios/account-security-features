##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
import re
import logging
_logger = logging.getLogger(__name__)


class AccountPaymentGroup(models.Model):
    _inherit = "account.payment.group"


    @api.multi
    def post(self):
        self.ensure_one()
        _logger.debug('======Payment Group======')
        if self.partner_type == 'supplier' and self.partner_id.apocryphal:
            raise ValidationError(_('This Partner is set as Apocryphal. Please verify the data'))
        return super(AccountPaymentGroup, self).post()
