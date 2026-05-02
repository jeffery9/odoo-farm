{
    'name': 'Farm Insurance',
    'version': '1.0',
    'category': 'Industries/Agriculture',
    'summary': 'Crop Yield Insurance Policies and Claims Management',
    'description': """
        Manages crop yield insurance policies, actuarial calculations, and claims processing.
        - US-58-16: Yield Insurance Actuarial Analysis and Claims
    """,
    'author': 'Gemini',
    'depends': [
        'farm_core',
        'farm_agri_science',
    ],
    'data': [
        'security/ir.model.access.csv',
        # 'data/ir_sequence_data.xml',
        # 'views/insurance_policy_views.xml',
        # 'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'AGPL-3',
}