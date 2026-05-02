with open('precision_production/views/mrp_production_views.xml', 'r') as f:
    content = f.read()

content = content.replace('<xpath expr="//sheet" position="inside">\n<div name="button_box" class="oe_button_box">', '<xpath expr="//div[@name=\'button_box\']" position="inside">')
content = content.replace('</button>\n            </div>\n            </xpath>', '</button>\n            </xpath>')

with open('precision_production/views/mrp_production_views.xml', 'w') as f:
    f.write(content)
    
with open('agri_precision_core/views/precision_bridge_views.xml', 'r') as f:
    content = f.read()

content = content.replace('<xpath expr="//sheet" position="inside">\\n                <div name="button_box" class="oe_button_box">', '<xpath expr="//div[@name=\'button_box\']" position="inside">')
content = content.replace('</div>\\n            </xpath>', '</xpath>')
content = content.replace('<xpath expr="//sheet" position="inside">\n<div name="button_box" class="oe_button_box">', '<xpath expr="//div[@name=\'button_box\']" position="inside">')
with open('agri_precision_core/views/precision_bridge_views.xml', 'w') as f:
    f.write(content)

