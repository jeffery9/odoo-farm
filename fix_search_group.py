with open('precision_production/views/phase_execution_views.xml', 'r') as f:
    content = f.read()

content = content.replace('<group expand="0" string="Group By">', '<separator/>')
content = content.replace('</group>\n            </search>', '</search>')

with open('precision_production/views/phase_execution_views.xml', 'w') as f:
    f.write(content)
