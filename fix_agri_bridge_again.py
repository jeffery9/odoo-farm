with open('agri_precision_core/views/precision_bridge_views.xml', 'r') as f:
    content = f.read()

content = content.replace('<xpath expr="//notebook" position="inside">\n                <page string="IoT Monitoring" invisible="not iot_device_ids">', '<xpath expr="//notebook" position="inside">\n                <page string="IoT Monitoring" invisible="not iot_device_ids">')
content = content.replace('</page>\n            </xpath>\n        </field>\n    </record>\n\n    <!-- Inject into Stock Lot', '</page>\n            </xpath>\n        </field>\n    </record>\n\n    <!-- Inject into Stock Lot')

# Let's just fix the whole file cleanly
