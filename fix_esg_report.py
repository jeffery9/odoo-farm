with open('farm_esg_report/models/__init__.py', 'r') as f:
    content = f.read()

content = content.replace("report_type = fields.Selection([\n        'annual', 'quarterly', 'sasb', 'gris', 'tcfd', 'custom', 'compliance', 'investor'\n    ]", "report_type = fields.Selection([\n        ('annual', 'Annual'), ('quarterly', 'Quarterly'), ('sasb', 'SASB'), ('gris', 'GRIS'), ('tcfd', 'TCFD'), ('custom', 'Custom'), ('compliance', 'Compliance'), ('investor', 'Investor')\n    ]")

with open('farm_esg_report/models/__init__.py', 'w') as f:
    f.write(content)

with open('farm_esg_report/models/__init__.py', 'r') as f:
    content = f.read()

content = content.replace("goal_type = fields.Selection([\n        'environmental', 'social', 'governance', 'integrated'\n    ]", "goal_type = fields.Selection([\n        ('environmental', 'Environmental'), ('social', 'Social'), ('governance', 'Governance'), ('integrated', 'Integrated')\n    ]")
content = content.replace("monitoring_frequency = fields.Selection([\n        'monthly', 'quarterly', 'semi_annually', 'annually'\n    ]", "monitoring_frequency = fields.Selection([\n        ('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('semi_annually', 'Semi Annually'), ('annually', 'Annually')\n    ]")
content = content.replace("sustainability_framework = fields.Selection([\n        'un_sdg', 'science_based_targets', 'b_corp', 'other'\n    ]", "sustainability_framework = fields.Selection([\n        ('un_sdg', 'UN SDG'), ('science_based_targets', 'Science Based Targets'), ('b_corp', 'B Corp'), ('other', 'Other')\n    ]")

with open('farm_esg_report/models/__init__.py', 'w') as f:
    f.write(content)
