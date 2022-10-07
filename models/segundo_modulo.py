# -*- coding: utf-8 -*- 
# Part of Odoo. See LICENSE file for full copyright and licensing details. 
from odoo import api, fields, models 
from datetime import datetime 
from .functions import *
import logging
_logger = logging.getLogger(__name__)
class segundo_modulo(models.Model): 
    _name = 'crc.segundo_modulo' 
    cadena = fields.Char(string='cadena')
    def siat_sincronization(self):
        records = 'WARNING01'
        response ='INFO01'
        _logger.warning("MiLog %s", records)
        _logger.info(response)
        print('CRON')
 
