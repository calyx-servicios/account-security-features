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


class ResPartnerApocryphalCron(models.Model):
    _name = "res.partner.apocryphal.cron"
    cron_date = fields.Date(string='Cron Date',default=fields.Datetime.now)
    apocryphal_ids=fields.One2many('res.partner.apocryphal','cron_id',string='Apocryphal')
    last = fields.Boolean(string='Last',default=False)

class ResPartnerApocryphal(models.Model):
    _name = "res.partner.apocryphal"

    cuit = fields.Char(string='cuit')
    apocryphal_date = fields.Date(string='Apocryphal Date')
    publication_date = fields.Date(string='Publication Date')
    partner_id = fields.Many2one('res.partner',string='Partner')
    cron_id = fields.Many2one('res.partner.apocryphal.cron',string='Cron')
    cron_date = fields.Date(related='cron_id.cron_date',string='Cron Date')
    cron_last = fields.Boolean(related='cron_id.last',string='Current')

    @api.multi
    def action_partner_cron_apocryphal(self):
        self.action_partner_cron_apocryphal_afip()
        self.action_partner_cron_apocryphal_reverse()
    
    @api.multi
    def action_partner_cron_apocryphal_reverse(self):
        _logger.debug('======>action_partner_check_apocryphal__reverse<======')
        for partner in self.env['res.partner'].search([('apocryphal', '=', True)]):
            partner.action_partner_check_apocryphal()


    @api.multi
    def action_partner_cron_apocryphal_afip(self):
        _logger.debug('======>action_partner_check_apocryphal<======')
        attachment=self.env['ir.attachment']
        filestore=attachment._filestore()
        _logger.debug('FileStore?====>%r',filestore)
        filename=filestore+'/invoices.zip'
        unzipfile=filestore+'/FacturasApocrifas.txt'
        urllib.request.urlretrieve("https://servicioscf.afip.gob.ar/Facturacion/facturasApocrifas/DownloadFile.aspx", filename)
        _logger.debug('======>Download Complete')
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall(filestore)
        _logger.debug('======>Unzip Complete')
        count=0
        partner_ids=[]
        #partner_apocryphal=self.env['res.partner.apocryphal']
        cron_date=date.today().strftime(DEFAULT_SERVER_DATE_FORMAT)

        with open(unzipfile, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            cron_id=self.env['res.partner.apocryphal.cron'].create({'last':True})
            for row in spamreader:
                
                cuit=row[0]
                if len(cuit)==11:
                    count+=1
                    _apocryphal_date=row[1]
                    _publication_date=row[2]
                    apocryphal_date_obj =None
                    publication_date_obj = None
                    try:
                        apocryphal_date_obj = datetime.datetime.strptime(_apocryphal_date, '%d/%m/%Y')
                        publication_date_obj = datetime.datetime.strptime(_publication_date, '%d/%m/%Y')
                    except:
                        pass
                    if apocryphal_date_obj and publication_date_obj:
                        _logger.debug('looking for [%r]=>%r', count, row[0])
                        partner_apocryphal = self.search([('cuit', '=', cuit),('apocryphal_date','=',apocryphal_date_obj)])
                        if not partner_apocryphal:
                            partner_apocryphal=self.create({
                                'cuit':cuit,
                                'apocryphal_date':apocryphal_date_obj,
                                'publication_date':publication_date_obj,
                                'cron_id': cron_id.id,
                                })
                            _logger.debug('partner_apocryphal Added=>%r',cuit)
                            
                        else:
                            partner_apocryphal.cron_id=cron_id.id
                            _logger.debug('partner_apocryphal Found=>%r',cuit)
                        
                        partner = self.env['res.partner'].search([('main_id_number', '=', cuit)])
                        if partner:
                            partner.action_partner_cron_apocryphal(cron_id.id)
        if count>0:
            for cron in self.env['res.partner.apocryphal.cron'].search([('id','!=',cron_id.id)]):
                cron.last=False

class ResPartner(models.Model):
    _inherit = "res.partner"

    apocryphal = fields.Boolean(string='Apocryphal',default=False,track_visibility='onchange')
    apocryphal_ids=fields.One2many('res.partner.apocryphal','partner_id',string='Apocryphal History')
    

    @api.multi
    def alert_apocryphal(self):
        _logger.debug('======>alert_apocryphal<======')
        self.ensure_one()
        subject='Partner Normalized'
        message='Normalize '
        if self.apocryphal:
            subject='Apocryphal Partner Detected'
            message='Apocryphal '
        message+="Partner  %s cuit:%s" % (self.name,self.main_id_number)
        user_ids=self.env['res.users'].search([('active','=',True)])
        self.env['mail.message'].create({'message_type':'notification',
                'body': message,
                'subject': subject,
                'needaction_partner_ids': [(4, user.partner_id.id, None) for user in user_ids],   
                'model': self._name,
                'res_id': self.id,
                })

    @api.multi
    def action_partner_check_apocryphal(self):
        self.action_partner_cron_apocryphal(cron_id=False)

    @api.multi
    def action_partner_cron_apocryphal(self, cron_id=False):
        _logger.debug('======>action_partner_check_apocryphal<======')
        self.ensure_one()
        partner_apocryphal=self.env['res.partner.apocryphal']
        if not cron_id:
            cron_id =self.env['res.partner.apocryphal.cron'].search([('last','=',True)]).ids
            if cron_id:
                cron_id=cron_id[0]
        _logger.debug('Apocryphal Data for Partner Found CRONID?====>%r',cron_id)
        partner = partner_apocryphal.search([('cuit', '=', self.main_id_number),('cron_id','=',cron_id)])
        _logger.debug('Apocryphal Data for Partner Found?====>%r',self.name)
        if partner:
            if not self.apocryphal:
                self.apocryphal=True
                partner.partner_id=self.id
                self.alert_apocryphal()
                _logger.debug('Now it is an Apocryphal Partner ====>%r',self.apocryphal)
        else:
            if self.apocryphal:
                self.apocryphal=False
                self.alert_apocryphal()
                _logger.debug('Now it is not an Apocryphal Partner Anymore ====>%r',self.apocryphal)
        _logger.debug('Apocryphal====>%r',self.apocryphal)
        
    


        
