with open('agri_precision_core/views/precision_bridge_views.xml', 'r') as f:
    content = f.read()

content = content.replace('</header>\n            </xpath>', '</xpath>')
content = content.replace('</header>\n            </xpath>', '</xpath>')
content = content.replace('</header>\n            </xpath>', '</xpath>')

# Wait, `</header>` is on line 60 but the previous replace didn't work because it had spaces or newlines.
content = content.replace('            </header>\n            </xpath>', '            </xpath>')

with open('agri_precision_core/views/precision_bridge_views.xml', 'w') as f:
    f.write(content)
