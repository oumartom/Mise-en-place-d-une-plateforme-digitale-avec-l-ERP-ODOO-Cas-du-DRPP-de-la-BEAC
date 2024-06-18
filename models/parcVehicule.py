# -- coding: utf-8 --

from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime, timedelta

class ParcVehicule(models.Model):
    _name = 'parc.vehicule'
    _description = """Gestion de parc des véhicules"""
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence asc'
    
    
    name = fields.Char(string="name")
    marque = fields.Selection(selection=[
        ('toyota', 'Toyota'),
        ('honda', 'Honda'),
        ('ford', 'Ford'),
        ('chevrolet','chevrolet'),
        ('nissan','nissan'),
        ('mercedes','mercedes'),
        ('hyundai','hyundai')
    ], string='Marque', required=True)
    modele = fields.Selection([
        ('corolla', 'Corolla'),
        ('camry', 'Camry'),
        ('rav4', 'RAV4'),
        ('tucson','tucson'),
        ('sonata','sonata'),
        ('A3','A3'),
        ('A4','A4'),
        ('C-class','C-class')
      
    ], string='Modèle', required=True)
    immatriculation = fields.Char(string="Immatriculation", required=True)
    # Contrainte SQL pour garantir l'unicité de l'immatriculation
    _sql_constraints = [
        ('immatriculation_unique', 'UNIQUE(immatriculation)', 'L\'immatriculation doit être unique !')
    ]
    sequence=fields.Integer()
    documents_ids = fields.One2many('parc.vehicule.document', 'vehicule_id', string='Documents')
    affectations_ids = fields.One2many('parc.vehicule.affectation', 'vehicule_id', string='Affectations')
    descrip = fields.Text('note')
    #employe_id = fields.Many2one('management.employee', string='Employé Affecté')
    agence_id = fields.Many2one('management.agence', string='Agence Affectée')
    pays_id = fields.Many2one('management.pays', string='Pays')
    Statut = fields.Selection([
        ('disponible', 'Disponible'),
        ('en_maintenance', 'En Maintenance'),
        ('affecté', 'Affectué')
    ], 'Statut', default='disponible')

    # def verifier_expiration_cartes_grises(self):
    #     today = fields.Date.today()
    #     vehicles_to_notify = self.search([('dateExpirationCarteGrise', '<=', today + timedelta(days=30)),
    #                                       ('dateExpirationCarteGrise', '>=', today)])
    #     for vehicle in vehicles_to_notify:
    #         vehicle.envoyer_notification_expiration()

    # def envoyer_notification_expiration(self):
    #     jours_restants = (self.dateExpirationCarteGrise - fields.Date.today()).days
    #     mail_message = (f"Cher utilisateur, <br/>"
    #                     f"Nous tenons à vous informer que la carte grise de votre véhicule <strong>{self.name}</strong> "
    #                     f"(Immatriculation: <strong>{self.immatriculation}</strong>) "
    #                     f"expire dans <strong>{jours_restants} jours</strong>.<br/>"
    #                     f"Veuillez prendre les mesures nécessaires pour la renouveler dans les plus brefs délais.<br/><br/>"
    #                     f"Cordialement,<br/>"
    #                     f"Votre équipe de gestion de parc automobile.")
    #     mail_values = {
    #         'subject': "Notification d'expiration de la carte grise",
    #         'body_html': mail_message,
    #         'email_to': 'oumartom45@gmail.com',  
    #     }
    #     self.env['mail.mail'].create(mail_values).send()

    # @api.model
    # def cron_verifier_expiration_cartes_grises(self):
    #     self.verifier_expiration_cartes_grises()
    
    
