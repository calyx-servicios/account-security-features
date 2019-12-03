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


class AccountInvoice(models.Model):
	_inherit = "account.invoice"

	@api.multi
	def action_invoice_open(self):
		self.ensure_one()
		if self.type in ('in_invoice', 'in_refund') and self.partner_id.apocryphal:
			raise ValidationError(_('This Partner is set as Apocryphal. Please verify the data'))
		return super(AccountInvoice, self).action_invoice_open()