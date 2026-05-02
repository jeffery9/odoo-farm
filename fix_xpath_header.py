with open('precision_production/views/product_views.xml', 'r') as f:
    content = f.read()

content = content.replace('<xpath expr="//header" position="inside">\n                <field name="production_drive_type" invisible="1"/>\n            </xpath>', '<xpath expr="//sheet" position="inside">\n                <field name="production_drive_type" invisible="1"/>\n            </xpath>')

with open('precision_production/views/product_views.xml', 'w') as f:
    f.write(content)
