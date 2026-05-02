import re

with open('agri_precision_core/views/precision_bridge_views.xml', 'r') as f:
    content = f.read()

# Replace <xpath expr="//header" position="inside">
# Since mrp.production form has a header, wait, did we say mrp.production doesn't have a header in Odoo 19?
# No, mrp.production HAS a header. In `precision_production`, we replaced `//header` with `//sheet` + `before` because we thought there was no header, and that worked!
# Let's do the exact same thing for `agri_precision_core`.
content = content.replace('<xpath expr="//header" position="inside">', '<xpath expr="//sheet" position="before">\n<header>')
content = content.replace('</xpath>\n            <xpath expr="//div[@name=\'button_box\']"', '</header>\n</xpath>\n            <xpath expr="//div[@name=\'button_box\']"')

# AND replace button_box inside sheet
content = content.replace('<xpath expr="//div[@name=\'button_box\']" position="inside">', '<xpath expr="//sheet" position="inside">\n<div name="button_box" class="oe_button_box">')
content = content.replace('</button>\n            </xpath>', '</button>\n</div>\n            </xpath>')

with open('agri_precision_core/views/precision_bridge_views.xml', 'w') as f:
    f.write(content)
