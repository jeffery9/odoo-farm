from odoo import models, fields, api, _
from datetime import datetime


class PerformanceDemoWizard(models.TransientModel):
    """
    Wizard to demonstrate the new Odoo 19 performance and security features
    """
    _name = 'agri.performance.demo.wizard'
    _description = 'Agricultural Performance Demo Wizard'

    demo_operation = fields.Selection([
        ('batch_processing', 'Batch Processing Demo'),
        ('precompute_demo', 'Precompute Feature Demo'),
        ('json_field_demo', 'JSON Field Demo'),
        ('security_demo', 'Security Enhancement Demo'),
        ('performance_monitoring', 'Performance Monitoring Demo')
    ], string="Demo Operation", required=True)

    record_count = fields.Integer(string="Record Count", default=100)
    demo_details = fields.Text(string="Demo Details", readonly=True)

    def run_demo(self):
        """
        Run the selected demo operation
        """
        if self.demo_operation == 'batch_processing':
            self._demo_batch_processing()
        elif self.demo_operation == 'precompute_demo':
            self._demo_precompute_feature()
        elif self.demo_operation == 'json_field_demo':
            self._demo_json_fields()
        elif self.demo_operation == 'security_demo':
            self._demo_security_enhancements()
        elif self.demo_operation == 'performance_monitoring':
            self._demo_performance_monitoring()

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Demo Completed',
                'message': f'Demo operation {self.demo_operation} completed successfully.',
                'sticky': False,
            }
        }

    def _demo_batch_processing(self):
        """
        Demonstrate batch processing capabilities
        """
        # This is a demo function - in real usage, this would process actual records
        self.demo_details = f"Running batch operation on {self.record_count} records...\n"

        # Example of using the batch operation mixin (if a model had it)
        # records = self.env['some.model'].search([], limit=self.record_count)
        # result = records.batch_operation(self._process_single_record, 50)

        self.demo_details += f"Batch demo completed for {self.record_count} records."

    def _demo_precompute_feature(self):
        """
        Demonstrate precompute feature usage
        """
        self.demo_details = "Demonstrating precompute feature...\n"

        # Simulate creating records with precompute fields
        for i in range(min(5, self.record_count)):  # Only demo a few records to keep it fast
            # Create a livestock production record that uses precompute
            record = self.env['farm.livestock.production'].create({
                'name': f'Demo Production Order {i}',
                'initial_total_weight': 100.0,
                'final_total_weight': 150.0,
                'product_qty': 10.0
            })

            # Verify that precompute worked by checking the value
            self.demo_details += f"Created record {record.name} with precomputed FCR: {record.fcr}\n"

            # Clean up the demo record
            record.unlink()

        self.demo_details += "Precompute demo completed."

    def _demo_json_fields(self):
        """
        Demonstrate JSON field capabilities
        """
        self.demo_details = "Demonstrating JSON field usage...\n"

        # Create a livestock production record with JSON config
        record = self.env['farm.livestock.production'].create({
            'name': 'JSON Demo Order',
            'livestock_config': {
                'feeding_schedule': ['morning', 'afternoon', 'evening'],
                'health_monitoring': True,
                'target_weight_gain': 1.5,
                'special_requirements': ['organic_feed', 'outdoor_access']
            },
            'initial_total_weight': 100.0,
            'final_total_weight': 150.0,
            'product_qty': 10.0
        })

        self.demo_details += f"Created record with JSON config: {record.livestock_config}\n"
        self.demo_details += f"Config type: {type(record.livestock_config)}\n"

        # Clean up the demo record
        record.unlink()
        self.demo_details += "JSON field demo completed."

    def _demo_security_enhancements(self):
        """
        Demonstrate security enhancements
        """
        self.demo_details = "Demonstrating security enhancements...\n"

        # Create a livestock production record that includes security features
        record = self.env['farm.livestock.production'].create({
            'name': 'Security Demo Order',
            'security_level': 'high',
            'initial_total_weight': 100.0,
            'final_total_weight': 150.0,
            'product_qty': 10.0
        })

        # Check that access was logged
        if record.access_log:
            self.demo_details += f"Security log created with {len(record.access_log)} entries\n"
        else:
            self.demo_details += "No access log entries found\n"

        # Clean up the demo record
        record.unlink()
        self.demo_details += "Security enhancement demo completed."

    def _demo_performance_monitoring(self):
        """
        Demonstrate performance monitoring
        """
        self.demo_details = "Demonstrating performance monitoring...\n"

        # Create a performance monitoring record
        monitor = self.env['agri.performance.monitor'].create({
            'name': 'Demo Operation',
            'model_name': 'wizard.demo',
            'operation': 'demo_run',
            'record_count': 1,
            'details': 'Demonstration of performance monitoring system',
            'status': 'completed'
        })

        self.demo_details += f"Created performance monitor: {monitor.name}\n"
        self.demo_details += f"Duration: {monitor.duration}s\n"

        # Clean up the demo record
        monitor.unlink()
        self.demo_details += "Performance monitoring demo completed."