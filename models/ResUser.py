from odoo import models, fields, api
class ResUsers(models.Model):
    _inherit = 'res.users'

    superieur_id = fields.Many2one('res.users', string="Supérieur Hiérarchique")
    departement_id = fields.Many2one('gestion_vehicule.departement', string="Département")
    # # Lien direct vers un seul employé
    # employee_id = fields.Many2one('management.employee', string="Linked Employee")

    # # Champ calculé pour l'agence basé sur l'employé lié
    # agence_id = fields.Many2one('management.agence', string="Agence", compute='_compute_agence_id', store=True)
    # job_title = fields.Char(string="Job Title")
    # @api.depends('employee_id.agence_id')
    # def _compute_agence_id(self):
    #     for user in self:
    #         user.agence_id = user.employee_id.agence_id.id if user.employee_id and user.employee_id.agence_id else None



# -- coding: utf-8 --

# from odoo import fields, models

# class ResUsers(models.Model):
#     _inherit = 'res.users'

#     agence_id = fields.Many2one(
#         'management.agence', 
#         string='Agence', 
#         help="Agence à laquelle cet utilisateur est associé."
#     )

# access_res_users_user,access_res_users_user,model_res_users,base.group_user,1,0,0,0
# access_res_users_admin,access_res_users_admin,model_res_users,base.group_system,1,1,1,1