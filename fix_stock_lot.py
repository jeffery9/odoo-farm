with open('farm_quality/views/stock_lot_views.xml', 'r') as f:
    content = f.read()

content = content.replace("<header>", '<xpath expr="//sheet" position="before">\n            <header>')
content = content.replace("</header>", '</header>\n            </xpath>')

with open('farm_quality/views/stock_lot_views.xml', 'w') as f:
    f.write(content)
