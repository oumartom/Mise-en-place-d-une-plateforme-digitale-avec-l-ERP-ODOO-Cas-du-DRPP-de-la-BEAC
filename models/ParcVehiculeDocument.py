# -- coding: utf-8 --

from odoo import models, fields, api
from datetime import timedelta
class ParcVehiculeDocument(models.Model):
    
    _name = 'parc.vehicule.document'
    _description = """Gestion de document des véhicules"""
    
   
    type_document = fields.Selection([
        ('carte_grise', 'Carte Grise'),
        ('assurance', 'Assurance'),
        ('controle_technique', 'Contrôle Technique')
        # Ajoutez d'autres types de documents si nécessaire
    ], string='Type de Document', required=True)

    date_emission = fields.Date(string='Date d\'Émission')
    date_expiration = fields.Date(string='Date d\'Expiration')
    vehicule_id = fields.Many2one('parc.vehicule', string='Véhicule Associé', ondelete='cascade')

    @api.model
    def notifier_expiration_documents(self):
        date_aujourdhui = fields.Date.today()
        date_limite = date_aujourdhui + timedelta(days=30)
        documents_expirant = self.search([('date_expiration', '<=', date_limite),
                                        ('date_expiration', '>=', date_aujourdhui)])
        
        for doc in documents_expirant:
            jours_restants = (doc.date_expiration - date_aujourdhui).days
            if doc.vehicule_id:
                utilisateurs = doc.vehicule_id.mapped('affectations_ids.utilisateur_id')
                for utilisateur in utilisateurs:
                    mail_values = {
                        'subject': f"[Important] Prochaine expiration du document : {doc.type_document}",
                        'body_html': f"""
                            <p>Bonjour {utilisateur.name},</p>
                            <p>Nous tenons à vous informer que le document '{doc.type_document}' associé au véhicule <strong>{doc.vehicule_id.name}</strong> (Immatriculation : <strong>{doc.vehicule_id.immatriculation}</strong>) arrive à expiration dans <strong>{jours_restants} jours</strong> (Date d'expiration : {doc.date_expiration}).</p>
                            <p>Il est important de prendre les mesures nécessaires avant cette date afin d'éviter toute interruption d'utilisation ou autres désagréments.</p>
                            <p>Pour toute information supplémentaire ou assistance, n'hésitez pas à nous contacter.</p>
                            <p>Cordialement,</p>
                            <p>Votre équipe de gestion de parc automobile</p>
                        """,
                        'email_to': utilisateur.email,
                    }
                    self.env['mail.mail'].create(mail_values).send()
