# -- coding: utf-8 --
from odoo import models, fields,api

class ParcVehiculeMaintenance(models.Model):
    _name = 'parc.vehicule.maintenance'
    _description = 'Maintenance de Véhicule'

    date_maintenance = fields.Date(string='Date de Maintenance', required=True)
    type_maintenance = fields.Selection([
        ('entretien', 'Entretien'),
        ('reparation', 'Réparation'),
        ('inspection', 'Inspection'),
        # Ajoutez d'autres types si nécessaire
    ], string='Type de Maintenance', required=True)
    cout = fields.Float(string='Coût')
    vehicule_id = fields.Many2one('parc.vehicule', string='Véhicule', ondelete='cascade')
    @api.model
    def create(self, vals):
        # Création de l'enregistrement de maintenance
        record = super(ParcVehiculeMaintenance, self).create(vals)

        # Mise à jour du statut du véhicule associé
        if record.vehicule_id:
            record.vehicule_id.write({'Statut': 'en_maintenance'})

        return record
