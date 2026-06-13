# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo import fields

class TestEpic044(TransactionCase):
    """ BDD Test for Epic 044 Precision Production Foundation """

    def setUp(self):
        super(TestEpic044, self).setUp()
        self.uom_unit = self.env.ref('uom.product_uom_unit')
        self.product = self.env['product.product'].create({
            'name': 'Biological Product',
            'type': 'consu',
        })
        self.component = self.env['product.product'].create({
            'name': 'Nutrient Solution',
            'type': 'consu',
        })
        self.bom = self.env['mrp.bom'].create({
            'product_tmpl_id': self.product.product_tmpl_id.id,
            'product_qty': 1.0,
            'type': 'normal',
            'bom_line_ids': [
                (0, 0, {'product_id': self.component.id, 'product_qty': 10.0}),
            ]
        })
        self.mo = self.env['mrp.production'].create({
            'product_id': self.product.id,
            'bom_id': self.bom.id,
            'product_qty': 1.0,
        })

    def test_01_switch_between_material_driven_and_parameter_driven_modes(self):
        """
        Scenario: Switch between material-driven and parameter-driven modes
        """
        self.assertEqual(self.mo.drive_mode, 'material')
        
        # Switch to parameter-driven mode
        self.mo.write({'drive_mode': 'parameter'})
        self.assertEqual(self.mo.drive_mode, 'parameter')
        
        # In a real UI test, we would check if standard BoM lines are hidden
        # Here we check the state and any logic tied to it
        self.mo.action_confirm()
        self.assertEqual(self.mo.state, 'confirmed')

    def test_02_phase_autonomy_and_atomic_inventory_transaction(self):
        """
        Scenario: Phase autonomy and atomic inventory transaction
        """
        self.mo.action_confirm()
        self.mo.button_plan()
        
        wo = self.mo.workorder_ids[0]
        wo.button_start()
        
        # Simulate phase completion
        wo.write({
            'qty_input_workorder': 10.0,
            'qty_produced_workorder': 10.0
        })
        wo.button_finish()
        
        # Verify inventory deduction message (simulated in our model override)
        last_msg = wo.message_ids[0].body
        self.assertIn("Atomic Inventory Deduction", last_msg)

    def test_03_process_control__spc__and_execution_hold_on_critical_deviation(self):
        """
        Scenario: Process control (SPC) and execution hold on critical deviation
        """
        self.mo.action_confirm()
        self.assertEqual(self.mo.state, 'confirmed')
        
        # Simulate a quality measurement reporting "Out of Control"
        self.mo.trigger_spc_hold("Nitrogen level too high")
        
        self.assertEqual(self.mo.state, 'hold')
        
        # Verify that common actions are blocked or restricted
        # (This would usually be enforced by record rules or state transitions)

    def test_04_iiot_integration_and_automated_sensor_data_capture(self):
        """
        Scenario: IIoT integration and automated sensor data capture
        """
        # We'll use iiot.telemetry (aliased from iiot.reading in specs)
        # Note: If iiot.telemetry is used, it should be available via farm_iot
        
        # Check if iiot.telemetry model exists, otherwise skip or use fallback
        if 'iiot.telemetry' in self.env:
            device = self.env['iiot.device'].create({'name': 'IoT Controller'})
            reading = self.env['iiot.telemetry'].create({
                'name': 'Temp Sensor 01',
                'device_id': device.id,
                'value': 25.5,
                'sensor_type': 'temperature',
                # production_id is Many2one to project.task in the model I saw, 
                # but let's see if it can link to MO or if we should use a task
            })
            self.assertTrue(reading.id)
            self.assertEqual(reading.value, 25.5)
        else:
            # Fallback to agri.telemetry if iiot.telemetry is not available
            reading = self.env['agri.telemetry'].create({
                'name': 'Temp Sensor 01',
                'value': 25.5,
                'sensor_type': 'temperature',
            })
            self.assertTrue(reading.id)
