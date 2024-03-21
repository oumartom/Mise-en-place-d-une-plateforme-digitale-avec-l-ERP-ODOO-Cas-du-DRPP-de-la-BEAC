# -*- coding: utf-8 -*-
{
    'name': 'Application Vehicules',
    'version': '1.0',
    'description': """ Module permettant de gérer la flotte de véhicules""",
    'category': 'Customizations',
    'website': 'https://www.votreentreprise.com',
    'depends': ['base', 'mail'],
    'application':True,
    'data':[
        'views/parcVehicule1.xml',
        'views/parcVehicule.xml',
        'security/ir.model.access.csv',
    ],
}