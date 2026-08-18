# -*- coding: utf-8 -*-
{
    'name': 'Agri-OS: Livestock Financial Valuation Bridge',
    'summary': 'Micro-industry bridge for livestock biomass valuation and dynamic credit lines',
    'version': '19.0.1.0.0',
    'category': 'Agri/Financial',
    'author': 'Agri-OS Team',
    'depends': [
        'farm_financial_valuation',  # Horizontal platform package (X-axis)
        'farm_livestock'             # Vertical industry package (Y-axis)
    ],
    'auto_install': True,            # Dual-factor auto-activation rule
    'data': [],
    'installable': True,
    'license': 'LGPL-3',
}
