import re

with open('farm_mushroom/views/mushroom_operation_views.xml', 'r') as f:
    content = f.read()

# Just leave a skeleton view
new_content = """<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_farm_mushroom_operation_form" model="ir.ui.view">
        <field name="name">farm.mushroom.operation.form</field>
        <field name="model">farm.mushroom.production</field>
        <field name="arch" type="xml">
            <form>
                <sheet>
                    <notebook>
                        <page string="Mushroom Cultivation Information" name="mushroom_info">
                            <group>
                                <field name="target_environmental_index"/>
                            </group>
                        </page>
                    </notebook>
                </sheet>
            </form>
        </field>
    </record>
</odoo>
"""
with open('farm_mushroom/views/mushroom_operation_views.xml', 'w') as f:
    f.write(new_content)

# Medicinal plants too
with open('farm_medicinal_plants/views/medicinal_plants_operation_views.xml', 'r') as f:
    content = f.read()
new_content2 = """<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_farm_medicinal_operation_form" model="ir.ui.view">
        <field name="name">farm.medicinal.operation.form</field>
        <field name="model">farm.medicinal.production</field>
        <field name="arch" type="xml">
            <form>
                <sheet>
                    <notebook>
                        <page string="Medicinal Cultivation Information" name="medicinal_info">
                            <group>
                                <field name="target_active_ingredient"/>
                            </group>
                        </page>
                    </notebook>
                </sheet>
            </form>
        </field>
    </record>
</odoo>
"""
with open('farm_medicinal_plants/views/medicinal_plants_operation_views.xml', 'w') as f:
    f.write(new_content2)
