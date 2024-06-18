# -- coding: utf-8 --

# from odoo import models, fields, api

# class Department(models.Model):
#     _name = 'management.departement'
    
#     name = fields.Char(string='Nom du departement', required=True)

from odoo import models, fields

class Departement(models.Model):
    _name = 'gestion_vehicule.departement'
    _description = 'Département'

    name = fields.Char(string="Nom")
    responsable_id = fields.Many2one('res.users', string="Responsable")
