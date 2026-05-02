with open('precision_production/views/phase_execution_views.xml', 'r') as f:
    content = f.read()

# Grouping tags inside search should be inside a <filter> or <group expand="0"> depending on Odoo version, 
# wait, in Odoo 19 `group expand="x"` etc is required under search, usually: <filter string="Group By" name="groupby" domain="[]" context="{'group_by': 'something'}"/>
# The RelaxNG error: `Invalid attribute string for element group`, `Element search has extra content: field`.
# Actually `<group string="Group By">` might not be allowed in Odoo 19 inside `<search>` without expand="0"?
# Let's replace `<group string="Group By">` with `<group expand="0" string="Group By">`

content = content.replace('<group string="Group By">', '<group expand="0" string="Group By">')

with open('precision_production/views/phase_execution_views.xml', 'w') as f:
    f.write(content)
