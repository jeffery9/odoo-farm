import re
with open('farm_marketing/views/farm_lot_views.xml', 'r') as f:
    content = f.read()

content = content.replace("                </button>\n            </xpath>", "                </button>\n                </div>\n            </xpath>")

with open('farm_marketing/views/farm_lot_views.xml', 'w') as f:
    f.write(content)
