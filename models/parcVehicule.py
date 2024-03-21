# -- coding: utf-8 --

from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime, timedelta

class ParcVehicule(models.Model):
    _name = 'parc.vehicule'
    _description = """Gestion de parc des véhicules"""
    
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
    immatriculation = fields.Char(string="immatriculation")
    dateEmissionCarteGrise = fields.Date(string='Date d\'émission')
    dateExpirationCarteGrise = fields.Date(string='Date d\'expiration')
    descrip = fields.Text('note')
    Statut = fields.Selection([
        ('disponible', 'Disponible'),
        ('en_maintenance', 'En Maintenance'),
        ('reserve', 'Réservé')
    ], 'Statut', default='disponible')

    @api.model
    def verifier_expiration_cartes_grises(self):
        today = fields.Date.today()
        vehicles_to_notify = self.search([('dateExpirationCarteGrise', '<=', today + timedelta(days=30)),
                                          ('dateExpirationCarteGrise', '>=', today)])
        for vehicle in vehicles_to_notify:
            vehicle.envoyer_notification_expiration()

    def envoyer_notification_expiration(self):
        mail_message = f"La carte grise du véhicule {self.name} (Immatriculation: {self.immatriculation}) expire bientôt."
        mail_values = {
            'subject': "Notification d'expiration de la carte grise",
            'body_html': "<p>{}</p>".format(mail_message),
            'email_to': 'oumartom45@gmail.com',
            # Optionnel: Vous pouvez spécifier 'email_from' si nécessaire
            # 'email_from': votre_adresse_email
        }
        self.env['mail.mail'].create(mail_values).send()