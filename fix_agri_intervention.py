with open('farm_operation/views/agri_intervention_views.xml', 'r') as f:
    content = f.read()

content = content.replace("                </page>\n            </xpath>", "                </page>\n                </notebook>\n            </xpath>")

with open('farm_operation/views/agri_intervention_views.xml', 'w') as f:
    f.write(content)
