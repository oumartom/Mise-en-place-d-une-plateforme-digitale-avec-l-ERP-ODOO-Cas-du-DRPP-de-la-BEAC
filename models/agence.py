# -- coding: utf-8 --

from odoo import models, fields, api

class Agence(models.Model):
    _name = 'management.agence'
    _description = 'Agence'

    name = fields.Char(string='Nom de l’Agence', required=True)
    pays_id = fields.Many2one('management.pays', string='Pays')
