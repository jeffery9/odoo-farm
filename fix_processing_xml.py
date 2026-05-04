import re
with open('farm_processing/views/farm_processing_views.xml', 'r') as f:
    content = f.read()

# Fix the first record 'mrp_bom_form_view_inherit_farm_proc'
# It seems I deleted too much or matched too broadly.
# Let's just fix the mismatched group.
content = content.replace('<group string="Mass Balance (US-04-02)">\n                            \n                            \n    </record>', '<group string="Mass Balance (US-04-02)">\n                        </group>\n                    </group>\n                </page>\n            </xpath>\n        </field>\n    </record>')

with open('farm_processing/views/farm_processing_views.xml', 'w') as f:
    f.write(content)
