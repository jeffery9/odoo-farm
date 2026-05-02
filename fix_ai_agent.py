import re

with open('farm_ai_agent/models/ai_coordination_layer.py', 'r') as f:
    content = f.read()

content = content.replace("industry_type = fields.Many2one('industry.type', string='Industry',", "industry_type = fields.Selection([\n        ('crop', 'Crop Farming'),\n        ('livestock', 'Livestock'),\n        ('aquaculture', 'Aquaculture'),\n        ('orchard', 'Orchard/Horticulture'),\n        ('processing', 'Processing'),\n    ], string='Industry',")

with open('farm_ai_agent/models/ai_coordination_layer.py', 'w') as f:
    f.write(content)

with open('farm_ai_agent/models/ai_decision_engine.py', 'r') as f:
    content = f.read()

content = content.replace("industry_type = fields.Many2one('industry.type', string='Industry')", "industry_type = fields.Selection([\n        ('crop', 'Crop Farming'),\n        ('livestock', 'Livestock'),\n        ('aquaculture', 'Aquaculture'),\n        ('orchard', 'Orchard/Horticulture'),\n        ('processing', 'Processing'),\n    ], string='Industry')")

with open('farm_ai_agent/models/ai_decision_engine.py', 'w') as f:
    f.write(content)
