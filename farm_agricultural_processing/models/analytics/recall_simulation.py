# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class AgriProcessingRecallSimulation(models.Model):
    """
    Recall Simulation and Traceability Test - US-14-22
    """
    _name = 'agri.processing.recall.simulation'
    _description = 'Recall Simulation and Traceability Test'

    name = fields.Char('Recall Simulation', required=True)
    simulation_date = fields.Date('Simulation Date', required=True, default=fields.Date.today())

    # Trigger source
    trigger_lot_id = fields.Many2one('stock.lot', string='Trigger Lot (Problem Source)')
    trigger_reason = fields.Text('Trigger Reason')

    # Forward trace (product distribution)
    affected_batches = fields.Many2many('stock.lot', 'recall_sim_batch_rel', 'simulation_id', 'batch_id', string='Affected Batches')
    affected_sales_orders = fields.Many2many('sale.order', 'recall_sim_so_rel', 'simulation_id', 'order_id', string='Affected Sales Orders')
    affected_customers = fields.Many2many('res.partner', 'recall_sim_partner_rel', 'simulation_id', 'partner_id', string='Affected Customers')

    # Backward trace (raw material source)
    source_materials = fields.Many2many('stock.lot', 'recall_sim_source_rel', 'simulation_id', 'source_id', string='Source Materials')
    source_suppliers = fields.Many2many('res.partner', 'recall_sim_supplier_rel', 'simulation_id', 'supplier_id', string='Source Suppliers')
    source_purchases = fields.Many2many('purchase.order', 'recall_sim_po_rel', 'simulation_id', 'order_id', string='Source Purchases')

    # Simulation results
    total_affected_qty = fields.Float('Total Affected Quantity', compute='_compute_affected_totals', store=True)
    total_affected_customers = fields.Integer('Total Affected Customers', compute='_compute_affected_totals', store=True)
    trace_depth_levels = fields.Integer('Trace Depth (Levels)', compute='_compute_trace_depth', store=True)

    # Report generation
    simulation_report = fields.Text('Simulation Report')
    report_generated = fields.Boolean('Report Generated', default=False)

    # Status and execution
    simulation_status = fields.Selection([
        ('draft', 'Draft'),
        ('executing', 'Executing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft')

    executor = fields.Many2one('res.users', string='Executed By', default=lambda self: self.env.user)
    execution_time = fields.Float('Execution Time (seconds)')

    notes = fields.Text('Simulation Notes')

    @api.model
    def create(self, vals):
        if 'name' not in vals or not vals['name']:
            vals['name'] = 'RECALL/' + fields.Date.to_string(fields.Date.today()) + '/' + str(self.id or 0)
        return super().create(vals)

    @api.depends('affected_batches', 'affected_customers')
    def _compute_affected_totals(self):
        for record in self:
            record.total_affected_qty = sum(record.affected_batches.mapped('product_qty'))
            record.total_affected_customers = len(record.affected_customers)

    @api.depends('source_materials', 'affected_batches')
    def _compute_trace_depth(self):
        for record in self:
            # Calculate the depth of traceability (number of production steps)
            # This would typically involve traversing the lot hierarchy
            record.trace_depth_levels = 0  # placeholder implementation

    def action_execute_recall_simulation(self):
        """Execute the recall simulation and generate report"""
        for record in self:
            record.simulation_status = 'executing'

            # This would contain complex logic to trace forward and backward through the supply chain
            # For now, we'll add a placeholder implementation
            affected_batches = []
            affected_customers = []
            source_materials = []
            source_suppliers = []

            # Forward trace from trigger lot
            if record.trigger_lot_id:
                # Find all derived lots (child lots)
                derived_lots = self._find_derived_lots(record.trigger_lot_id)
                affected_batches = derived_lots

                # Find sales orders with these lots
                affected_sales = self.env['sale.order'].search([
                    ('order_line.move_ids.move_line_ids.lot_id', 'in', [l.id for l in derived_lots])
                ])
                affected_customers = affected_sales.mapped('partner_id')

                # Backward trace to find sources
                source_lots = self._find_source_lots(record.trigger_lot_id)
                source_materials = source_lots

                # Find suppliers of source materials
                source_purchases = self.env['purchase.order'].search([
                    ('order_line.move_ids.move_line_ids.lot_id', 'in', [l.id for l in source_lots])
                ])
                source_suppliers = source_purchases.mapped('partner_id')

            # Update the record with the traced data
            record.affected_batches = [(6, 0, [l.id for l in affected_batches])]
            record.affected_customers = [(6, 0, [c.id for c in affected_customers])]
            record.source_materials = [(6, 0, [l.id for l in source_materials])]
            record.source_suppliers = [(6, 0, [s.id for s in source_suppliers])]

            # Generate the report
            report = self._generate_recall_report(record)
            record.simulation_report = report
            record.report_generated = True
            record.simulation_status = 'completed'

            # Calculate execution time (placeholder)
            record.execution_time = 0.5

        return True

    def _find_derived_lots(self, trigger_lot):
        """Find all lots derived from the trigger lot (forward trace)"""
        # This is a simplified version - in practice would need to traverse through MRP productions
        lots_to_check = [trigger_lot]
        all_derived_lots = [trigger_lot]

        while lots_to_check:
            current_lot = lots_to_check.pop(0)
            # Find productions that used this lot as input
            productions = self.env['mrp.production'].search([
                ('move_raw_ids.move_line_ids.lot_id', '=', current_lot.id)
            ])

            # Get the output lots from these productions
            output_lots = productions.mapped('move_finished_ids.move_line_ids.lot_id')
            for lot in output_lots:
                if lot not in all_derived_lots:
                    all_derived_lots.append(lot)
                    lots_to_check.append(lot)

        return all_derived_lots

    def _find_source_lots(self, trigger_lot):
        """Find all source lots for the trigger lot (backward trace)"""
        lots_to_check = [trigger_lot]
        all_source_lots = [trigger_lot]

        while lots_to_check:
            current_lot = lots_to_check.pop(0)
            # Find the parent lot if it exists
            if current_lot.parent_lot_id and current_lot.parent_lot_id not in all_source_lots:
                all_source_lots.append(current_lot.parent_lot_id)
                lots_to_check.append(current_lot.parent_lot_id)

        return all_source_lots

    def _generate_recall_report(self, record):
        """Generate a recall simulation report"""
        report = f"""
RECALL SIMULATION REPORT
========================
Date: {record.simulation_date}
Trigger Lot: {record.trigger_lot_id.name if record.trigger_lot_id else 'N/A'}
Trigger Reason: {record.trigger_reason or 'N/A'}

FORWARD TRACE (Distribution Chain):
- Affected Batches: {len(record.affected_batches)}
- Affected Customers: {len(record.affected_customers)}
- Total Affected Quantity: {record.total_affected_qty} units

BACKWARD TRACE (Supply Chain):
- Source Materials: {len(record.source_materials)}
- Source Suppliers: {len(record.source_suppliers)}

TRACEABILITY DEPTH: {record.trace_depth_levels} levels

This simulation demonstrates the system's capability to perform rapid recall analysis
as required by food safety regulations. All results are traceable to original
production orders and can be exported for regulatory audit purposes.
        """
        return report.strip()


class AgriProcessingPerformanceAnalytics(models.Model):
    """
    Performance and Efficiency Analytics - US-14-16
    """
    _name = 'agri.processing.performance.analytics'
    _description = 'Performance and Efficiency Analytics'

    name = fields.Char('Performance Record', required=True)
    production_id = fields.Many2one('farm.processing.production', string='Production Order', required=True)
    analysis_date = fields.Date('Analysis Date', default=fields.Date.today())

    # Efficiency metrics
    overall_equipment_effectiveness = fields.Float('OEE (%)')
    production_efficiency = fields.Float('Production Efficiency (%)')
    resource_utilization_rate = fields.Float('Resource Utilization Rate (%)')

    # Time-based metrics
    planned_production_time = fields.Float('Planned Production Time (hours)')
    actual_production_time = fields.Float('Actual Production Time (hours)')
    downtime_hours = fields.Float('Downtime (hours)')

    # Quality metrics
    first_pass_yield = fields.Float('First Pass Yield (%)')
    defect_rate = fields.Float('Defect Rate (%)')

    # Cost metrics
    cost_per_unit = fields.Float('Cost Per Unit')
    total_production_cost = fields.Float('Total Production Cost')

    # Analysis notes
    analysis_notes = fields.Text('Analysis Notes')

    @api.model
    def create(self, vals):
        if 'name' not in vals or not vals['name']:
            vals['name'] = 'PERF/' + fields.Date.to_string(fields.Date.today()) + '/' + str(self.id or 0)
        return super().create(vals)