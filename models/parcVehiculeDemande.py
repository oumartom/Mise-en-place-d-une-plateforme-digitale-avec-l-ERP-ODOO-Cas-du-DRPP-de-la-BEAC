
# # -- coding: utf-8 --
# from odoo import models, fields, api
# from odoo.exceptions import ValidationError

# class ParcVehiculeDemande(models.Model):
    
#     _name = 'parc.vehicule.demande'
#     _description = 'Demande de Véhicule'
#     _inherit = ['mail.thread', 'mail.activity.mixin']

#     date_demande = fields.Date(string='Date de Demande', default=fields.Date.today, readonly=True)
#     demandeur_id = fields.Many2one('res.users', string='Demandeur', default=lambda self: self.env.user, readonly=True)
#     vehicule_id = fields.Many2one('parc.vehicule', string='Véhicule', domain=[('Statut', '=', 'disponible')])
#     date_debut = fields.Date(string='Date de Début', required=True)
#     date_fin = fields.Date(string='Date de Fin', required=True, tracking=True)
#     raison = fields.Text(string='Raison de la Demande')
#     etat = fields.Selection([
#         ('nouveau', 'Nouveau'),
#         ('soumis', 'Soumis'),
#         ('approuve', 'Approuvé'),
#         ('refuse', 'Refusé'),
#     ], string='État', default='nouveau', readonly=True)

#     supervisor_email = fields.Char(string='E-mail du Supérieur Hiérarchique', default='tom.oumar@facsciences-uy1.cm')

#     def action_approve(self):
#         for record in self:
#             if record.vehicule_id.Statut != 'disponible':
#                 raise ValidationError("Le véhicule n'est pas disponible.")

#             record.write({'etat': 'approuve'})
#             record.vehicule_id.write({'Statut': 'affecté'})

#             # Envoyer une notification au demandeur et à l'administration
#             record.message_post(
#                 body="Votre demande de véhicule a été approuvée.",
#                 message_type='email',
#                 subtype_xmlid='mail.mt_comment',  # sous-type XML ID pour les commentaires
#                 partner_ids=[(4, record.demandeur_id.partner_id.id), (4, self.env.ref('base.user_admin').partner_id.id)]
#             )

#     def action_refuse(self):
#         for record in self:
#             record.write({'etat': 'refuse'})
#             # Envoyer une notification au demandeur
#             record.message_post(
#                 body="Votre demande de véhicule a été refusée.",
#                 message_type='email',
#                 subtype_xmlid='mail.mt_comment',  # sous-type XML ID pour les commentaires
#                 partner_ids=[(4, record.demandeur_id.partner_id.id)]
#             )

#     @api.model
#     def create(self, vals):
#         new_demande = super(ParcVehiculeDemande, self).create(vals)
        
#         # Envoyer une notification à l'adresse e-mail du supérieur hiérarchique
#         new_demande.message_post(
#             body="Une nouvelle demande de véhicule a été créée.",
#             message_type='email',
#             subtype_xmlid='mail.mt_comment',  # sous-type XML ID pour les commentaires
#             email_from=self.env.user.email_formatted,
#             email_to=new_demande.supervisor_email
#         )

#         return new_demande

# -- coding: utf-8 --
from odoo import models, fields, api
from odoo.exceptions import ValidationError
class ParcVehiculeDemande(models.Model):
    _name = 'parc.vehicule.demande'
    _description = 'Demande de Véhicule'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    date_demande = fields.Date(string='Date de Demande', default=fields.Date.today, readonly=True)
    demandeur_id = fields.Many2one('res.users', string='Demandeur', default=lambda self: self.env.user, readonly=True)
    vehicule_id = fields.Many2one('parc.vehicule', string='Véhicule', domain=[('Statut', '=', 'disponible')])
    date_debut = fields.Date(string='Date de Début', required=True)
    date_fin = fields.Date(string='Date de Fin', required=True, tracking=True)
    raison = fields.Text(string='Raison de la Demande')
    etat = fields.Selection([
        ('nouveau', 'Nouveau'),
        ('soumis', 'Soumis'),
        ('approuve', 'Approuvé'),
        ('refuse', 'Refusé'),
    ], string='État', default='nouveau', readonly=True)

    supervisor_email = fields.Char(string='E-mail du Supérieur Hiérarchique', default='tom.oumar@facsciences-uy1.cm')

    def action_approve(self):
        for record in self:
            if record.vehicule_id.Statut != 'disponible':
                raise ValidationError("Le véhicule n'est pas disponible.")

            record.write({'etat': 'approuve'})
            record.vehicule_id.write({'Statut': 'affecté'})
            # Création automatique de l'affectation
            self.env['parc.vehicule.affectation'].create({
                'vehicule_id': record.vehicule_id.id,
                'utilisateur_id': record.demandeur_id.id,
                'date_debut': record.date_debut,
                'date_fin': record.date_fin
            })

            # Envoyer une notification au demandeur et à l'administration
            record.message_post(
                body="Votre demande de véhicule a été approuvée.",
                message_type='email',
                subtype_xmlid='mail.mt_comment',  # sous-type XML ID pour les commentaires
                partner_ids=[record.demandeur_id.partner_id.id, self.env.ref('base.user_admin').partner_id.id]
            )

    def action_refuse(self):
        for record in self:
            record.write({'etat': 'refuse'})
            # Envoyer une notification au demandeur
            record.message_post(
                body="Votre demande de véhicule a été refusée.",
                message_type='email',
                subtype_xmlid='mail.mt_comment',  # sous-type XML ID pour les commentaires
                partner_ids=[record.demandeur_id.partner_id.id]
            )

    @api.model
    def create(self, vals):
        new_demande = super(ParcVehiculeDemande, self).create(vals)
        
        # Message pour l'administrateur
        admin = self.env.ref('base.user_admin')
        message_admin = "Une nouvelle demande de véhicule a été créée par {}.".format(new_demande.demandeur_id.name)
        
        # Envoi du message sous forme d'email
        new_demande.message_post(
            body=message_admin,
            author_id=admin.partner_id.id,
            message_type='email',
            subtype_xmlid='mail.mt_comment'  # sous-type XML ID pour les commentaires
        )

        return new_demande

