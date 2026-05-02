with open('agri_precision_core/views/precision_bridge_views.xml', 'r') as f:
    content = f.read()

# 1. header -> sheet before
content = content.replace('<xpath expr="//header" position="inside">', '<xpath expr="//sheet" position="before">\n<header>')
content = content.replace('</button>\n            </xpath>\n            <xpath expr="//div[@name=\'button_box\']"', '</button>\n</header>\n            </xpath>\n            <xpath expr="//div[@name=\'button_box\']"')

# 2. Fix the buttons in header
content = content.replace('name="action_update_yield_estimate"', 'name="action_update_yield_estimate_btn"')
content = content.replace('name="action_apply_agri_intervention"', 'name="action_apply_agri_intervention_btn"')

# 3. Fix button_box -> sheet inside
content = content.replace('<xpath expr="//div[@name=\'button_box\']" position="inside">', '<xpath expr="//sheet" position="inside">\n<div name="button_box" class="oe_button_box">')
# Close button box properly
content = content.replace('</button>\n            </xpath>\n            <xpath expr="//field[@name=\'product_qty\']"', '</button>\n</div>\n            </xpath>\n            <xpath expr="//field[@name=\'product_qty\']"')

# 4. Fix notebook in stock.lot
content = content.replace('<xpath expr="//notebook" position="inside">', '<xpath expr="//sheet" position="inside">\n<notebook>')
content = content.replace('</page>\n            </xpath>\n        </field>', '</page>\n</notebook>\n            </xpath>\n        </field>')

with open('agri_precision_core/views/precision_bridge_views.xml', 'w') as f:
    f.write(content)
