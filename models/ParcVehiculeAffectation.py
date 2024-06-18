# -- coding: utf-8 --
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ParcVehiculeAffectation(models.Model):
    _name = 'parc.vehicule.affectation'
    _description = 'Affectation de Véhicule'

    date_debut = fields.Date(string='Date de Début', required=True)
    date_fin = fields.Date(string='Date de Fin', required=True)
    utilisateur_id = fields.Many2one('res.users', string='Utilisateur', required=True)
    vehicule_id = fields.Many2one('parc.vehicule', string='Véhicule', required=True, domain=[('Statut', '=', 'disponible')])

    @api.model
    def create(self, vals):
        vehicule = self.env['parc.vehicule'].browse(vals['vehicule_id'])
        
        if vehicule.Statut != 'disponible':
            raise ValidationError("Ce véhicule n'est pas disponible pour l'affectation.")
        
        # Vérifiez si le véhicule est déjà affecté à quelqu'un d'autre pendant cette période
        affectations = self.search([
            ('vehicule_id', '=', vals['vehicule_id']),
            ('date_debut', '<=', vals['date_fin']),
            ('date_fin', '>=', vals['date_debut'])
        ])

        if affectations:
            raise ValidationError("Ce véhicule est déjà affecté à quelqu'un d'autre pendant cette période.")

        return super(ParcVehiculeAffectation, self).create(vals)
    
    @api.model
    def create(self, vals):
        # ... vérifications existantes ...
        record = super(ParcVehiculeAffectation, self).create(vals)
        if record.vehicule_id:
            record.vehicule_id.write({'Statut': 'affecté'})
        return record

    def unlink(self):
        for record in self:
            if record.vehicule_id:
                record.vehicule_id.write({'Statut': 'disponible'})
        return super(ParcVehiculeAffectation, self).unlink()
