from odoo import models, fields, api

class ParcVehiculeDashboard(models.Model):
    _name = 'parc.vehicule.dashboard'
    _description = 'Dashboard pour la gestion de parc automobile'

    total_vehicles = fields.Integer(compute="_compute_vehicle_stats", string="Total Véhicules")
    vehicles_in_maintenance = fields.Integer(compute="_compute_vehicle_stats", string="Véhicules en Maintenance")
    vehicles_available = fields.Integer(compute="_compute_vehicle_stats", string="Véhicules Disponibles")
    demandes_graph = fields.Binary(string="Graphique des Demandes")
    expiring_documents = fields.Many2many('parc.vehicule.document', string="Documents Expirants")

    @api.depends()  # Rien dans depends
    def _compute_vehicle_stats(self):
        for record in self:
            record.total_vehicles = self.env['parc.vehicule'].search_count([])
            record.vehicles_in_maintenance = self.env['parc.vehicule'].search_count([('statut', '=', 'en_maintenance')])
            record.vehicles_available = self.env['parc.vehicule'].search_count([('statut', '=', 'disponible')])
