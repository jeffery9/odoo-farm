with open('agri_precision_core/views/precision_bridge_views.xml', 'r') as f:
    content = f.read()

# Replace <xpath expr="//header" position="inside"> ... </xpath>
content = content.replace('<xpath expr="//header" position="inside">\n                <button name="action_update_yield_estimate" string="Calibrate Yield" type="object" class="btn-secondary"/>\n                <button name="action_apply_agri_intervention" string="Apply Agri Intervention" type="object" class="btn-warning" context="{\'default_intervention_type\': \'manual\', \'default_description\': \'Manual intervention applied\'}"/>\n            </xpath>',
'''<xpath expr="//sheet" position="before">
    <header>
        <button name="action_update_yield_estimate_btn" string="Calibrate Yield" type="object" class="btn-secondary"/>
        <button name="action_apply_agri_intervention_btn" string="Apply Agri Intervention" type="object" class="btn-warning" context="{'default_intervention_type': 'manual', 'default_description': 'Manual intervention applied'}"/>
    </header>
</xpath>''')

# Replace <xpath expr="//div[@name='button_box']" position="inside"> ... </xpath>
content = content.replace('''<xpath expr="//div[@name='button_box']" position="inside">
                <button class="oe_stat_button" icon="fa-stethoscope">
                    <div class="o_stat_info">
                        <span class="o_stat_value"><field name="intervention_count"/></span>
                        <span class="o_stat_text">Interventions</span>
                    </div>
                </button>
                <button class="oe_stat_button" icon="fa-bolt" invisible="not iot_device_ids">
                    <div class="o_stat_info">
                        <field name="iot_status" widget="badge"
                               decoration-success="iot_status == 'normal'"
                               decoration-info="iot_status == 'monitoring'"
                               decoration-warning="iot_status == 'warning'"
                               decoration-danger="iot_status == 'critical'"/>
                        <span class="o_stat_text">IoT Status</span>
                    </div>
                </button>
            </xpath>''', '''<xpath expr="//sheet" position="inside">
    <div name="button_box" class="oe_button_box">
        <button class="oe_stat_button" icon="fa-stethoscope">
            <div class="o_stat_info">
                <span class="o_stat_value"><field name="intervention_count"/></span>
                <span class="o_stat_text">Interventions</span>
            </div>
        </button>
        <button class="oe_stat_button" icon="fa-bolt" invisible="not iot_device_ids">
            <div class="o_stat_info">
                <field name="iot_status" widget="badge"
                       decoration-success="iot_status == 'normal'"
                       decoration-info="iot_status == 'monitoring'"
                       decoration-warning="iot_status == 'warning'"
                       decoration-danger="iot_status == 'critical'"/>
                <span class="o_stat_text">IoT Status</span>
            </div>
        </button>
    </div>
</xpath>''')

# Replace <xpath expr="//notebook" position="inside">
# Looking at stock.lot, we should just inject <notebook> into <sheet>
content = content.replace('<xpath expr="//notebook" position="inside">', '<xpath expr="//sheet" position="inside">\n<notebook>')
content = content.replace('</page>\n            </xpath>', '</page>\n</notebook>\n            </xpath>')

with open('agri_precision_core/views/precision_bridge_views.xml', 'w') as f:
    f.write(content)
