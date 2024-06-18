# -- coding: utf-8 --

from odoo import models, fields, api

class Direction(models.Model):
    _name = 'management.direction'
    
    name = fields.Char(string='Nom de la direction', required=True)