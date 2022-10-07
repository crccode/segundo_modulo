# -*- coding: utf-8 -*- 
# Part of Odoo. See LICENSE file for full copyright and licensing details. 
from odoo import api, fields, models 
from datetime import datetime 

class segundo_modulo(models.Model): 
    _name = 'crc.segundo_modulo' 
    cadena = fields.Char(string='cadena') 
 
