# -- coding: utf-8 --

from odoo import models, fields, api

class Service(models.Model):
    _name = 'management.service'
    
    name = fields.Char(string='Nom du service', required=True)