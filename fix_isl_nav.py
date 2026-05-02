import re
with open('farm_mrp/views/mrp_isl_navigation_views.xml', 'r') as f:
    content = f.read()

content = re.sub(r'<record id="view_mrp_bom_line_tree_isl_nav"[\s\S]*?</record>', '<!-- view_mrp_bom_line_tree_isl_nav removed -->', content)

with open('farm_mrp/views/mrp_isl_navigation_views.xml', 'w') as f:
    f.write(content)
