# -- coding: utf-8 --

from odoo import models, fields, api

class Pays(models.Model):
    _name = 'management.pays'
    _description = 'Pays'

    name = fields.Char(string='Nom du Pays', required=True)
    agence_ids = fields.One2many('management.agence', 'pays_id', string='Agences')
