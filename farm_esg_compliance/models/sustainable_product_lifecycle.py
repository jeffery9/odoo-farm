from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class AgriSustainableProductLifecycle(models.Model):
    """
    US-101-05: Sustainable Product Lifecycle Management
    Model for managing products from design to end-of-life, considering triple bottom line throughout the lifecycle.
    """
    _name = 'agri.sustainable.product.lifecycle'
    _description = 'Agricultural Sustainable Product Lifecycle'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Product Lifecycle Name', required=True)
    product_id = fields.Many2one('product.template', string='Product', required=True)
    lot_id = fields.Many2one('stock.lot', string='Batch/Lot')

    # Lifecycle stages
    lifecycle_stage = fields.Selection([
        ('design', 'Design'),
        ('development', 'Development'),
        ('production', 'Production'),
        ('distribution', 'Distribution'),
        ('consumption', 'Consumption'),
        ('end_of_life', 'End of Life'),
    ], string='Lifecycle Stage', default='design')

    # Triple bottom line metrics throughout lifecycle
    economic_impact = fields.Float('Economic Impact Score (0-100)')
    environmental_impact = fields.Float('Environmental Impact Score (0-100)')
    social_impact = fields.Float('Social Impact Score (0-100)')
    lifecycle_sustainability_score = fields.Float('Lifecycle Sustainability Score (0-100)',
                                                  compute='_compute_lifecycle_score', store=True)

    # Design principles
    design_principles = fields.Text('Design Principles')
    sustainability_guidelines = fields.Text('Sustainability Guidelines')
    optimization_suggestions = fields.Text('Optimization Suggestions')

    # Ancestry tracking (US-101-05 requirement)
    genetic_lineage = fields.Text('Genetic Lineage/Origin')
    production_ancestry = fields.Text('Production Ancestry')
    complete_lineage_trace = fields.Text('Complete Lineage Trace')

    # Lifecycle management
    start_date = fields.Date('Lifecycle Start Date')
    expected_lifespan = fields.Float('Expected Lifespan (Days)')
    current_age = fields.Float('Current Age (Days)', compute='_compute_current_age', store=True)

    # End-of-life management
    end_of_life_plan = fields.Selection([
        ('waste', 'Waste Disposal'),
        ('recycle', 'Recycling'),
        ('compost', 'Composting'),
        ('repurpose', 'Repurposing'),
        ('circular', 'Circular Market'),
    ], string='End of Life Plan', default='waste')

    # Integration with circular economy
    circular_market_ready = fields.Boolean('Circular Market Ready')
    circular_market_listing_id = fields.Many2one('agri.sustainability.circular.flow',
                                                 string='Circular Market Listing')

    # Status and control
    status = fields.Selection([
        ('active', 'Active'),
        ('monitored', 'Monitored'),
        ('optimizing', 'Optimizing'),
        ('end_of_life', 'End of Life'),
        ('transitioning', 'Transitioning'),
    ], string='Status', default='active')

    # Lifecycle events
    lifecycle_events = fields.Text('Lifecycle Events Log')

    # Related entities
    farm_id = fields.Many2one('farm.location', string='Farm Location')
    supplier_ids = fields.Many2many('res.partner', string='Input Suppliers')

    @api.depends('economic_impact', 'environmental_impact', 'social_impact')
    def _compute_lifecycle_score(self):
        for record in self:
            if record.economic_impact and record.environmental_impact and record.social_impact:
                record.lifecycle_sustainability_score = (record.economic_impact +
                                                        record.environmental_impact +
                                                        record.social_impact) / 3
            else:
                record.lifecycle_sustainability_score = 0.0

    @api.depends('start_date')
    def _compute_current_age(self):
        from datetime import date
        for record in self:
            if record.start_date:
                start_date = fields.Date.from_string(record.start_date)
                record.current_age = (date.today() - start_date).days
            else:
                record.current_age = 0.0

    @api.model
    def create(self, vals):
        record = super().create(vals)

        # Initialize the complete lineage trace with product and lot information
        if record.product_id:
            record.complete_lineage_trace = f"""
Product: {record.product_id.name}
Product ID: {record.product_id.id}
Product Category: {record.product_id.categ_id.name if record.product_id.categ_id else 'N/A'}

Genetic Lineage: {record.genetic_lineage or 'Not specified'}
Production Ancestry: {record.production_ancestry or 'Not specified'}
Farm: {record.farm_id.name if record.farm_id else 'Not specified'}
Suppliers: {', '.join([s.name for s in record.supplier_ids]) if record.supplier_ids else 'Not specified'}

Lifecycle created on: {fields.Date.context_today(record)}
            """

        return record

    def action_update_lifecycle_stage(self):
        """Update the lifecycle stage based on current age and other factors"""
        for record in self:
            if not record.start_date:
                record.start_date = fields.Date.context_today(record)

            # Determine stage based on age and other factors
            max_age = record.expected_lifespan or 365  # Default to 1 year if not specified

            if record.current_age < max_age * 0.1:
                new_stage = 'design'
            elif record.current_age < max_age * 0.3:
                new_stage = 'development'
            elif record.current_age < max_age * 0.7:
                new_stage = 'production'
            elif record.current_age < max_age * 0.9:
                new_stage = 'distribution'
            elif record.current_age < max_age:
                new_stage = 'consumption'
            else:
                new_stage = 'end_of_life'

            record.lifecycle_stage = new_stage

            # Add to lifecycle events
            if record.lifecycle_events:
                record.lifecycle_events += f"\n{fields.Date.context_today(record)}: Stage updated to {new_stage}"
            else:
                record.lifecycle_events = f"{fields.Date.context_today(record)}: Stage updated to {new_stage}"

    def action_plan_end_of_life(self):
        """Plan for end-of-life management based on US-101-05 requirements"""
        for record in self:
            # When approaching end of life, check for circular options
            if record.current_age >= record.expected_lifespan * 0.9:
                if record.circular_market_ready:
                    record.end_of_life_plan = 'circular'
                    record.status = 'transitioning'

                    # Create a circular market listing if not exists
                    if not record.circular_market_listing_id:
                        circular_flow = self.env['agri.sustainability.circular.flow'].create({
                            'name': f'Circular Market - {record.name}',
                            'code': self.env['ir.sequence'].next_by_code('agri.sustainability.circular.flow') or '/',
                            'flow_type': 'waste_to_resource',
                            'input_product_id': record.product_id.id,
                            'output_product_id': record.product_id.id,  # Same product for recycling
                            'input_quantity': 1.0,  # Placeholder
                            'output_quantity': 1.0,  # Placeholder
                        })
                        record.circular_market_listing_id = circular_flow
                else:
                    record.status = 'end_of_life'

    def action_generate_optimization_suggestions(self):
        """Generate optimization suggestions based on triple bottom line"""
        for record in self:
            suggestions = []

            if record.economic_impact < 60:
                suggestions.append("Consider cost optimization strategies or premium pricing for sustainable products.")

            if record.environmental_impact < 60:
                suggestions.append("Implement more sustainable production methods or renewable resource usage.")

            if record.social_impact < 60:
                suggestions.append("Enhance community engagement or fair trade practices in the supply chain.")

            if record.circular_market_ready == False:
                suggestions.append("Consider preparing for circular economy options to improve end-of-life sustainability.")

            record.optimization_suggestions = '\n'.join(suggestions) if suggestions else "No specific optimization suggestions at this time."

    def action_apply_design_principles(self):
        """Apply sustainable design principles"""
        for record in self:
            principles = f"""
Sustainable Design Principles for {record.product_id.name if record.product_id else record.name}:

1. Resource Efficiency: Minimize resource consumption during production
2. Renewable Inputs: Use renewable or recycled materials where possible
3. Energy Efficiency: Optimize energy usage throughout lifecycle
4. Waste Reduction: Minimize waste generation at all stages
5. Circular Design: Design for reuse, repair, and recycling
6. Local Sourcing: Prioritize local suppliers to reduce transportation impact
7. Biodegradability: Ensure materials can safely return to environment
8. Durability: Maximize useful life of the product
            """
            record.design_principles = principles

    def action_monitor_lifecycle(self):
        """[US-101-05] Monitor lifecycle and automate Lot-Ancestry traceability"""
        for record in self:
            if record.lot_id:
                # Automate Lot Ancestry Traceability
                record.production_ancestry = f"Lot Ancestry: {record.lot_id.name}. Quality Fingerprint: {record.lot_id.quality_fingerprint or 'Pending'}"
                record.environmental_impact = record.lot_id.environmental_impact
                record.social_impact = record.lot_id.social_impact
                record.economic_impact = record.lot_id.economic_impact

            record.status = 'monitored'
            monitoring_event = f"\n{fields.Date.context_today(record)}: Lifecycle monitored. DNA inherited from Lot {record.lot_id.name if record.lot_id else 'N/A'}"
            record.lifecycle_events = (record.lifecycle_events or "") + monitoring_event

    def action_transition_to_circular(self):
        """[US-101-05] Automated Circular-End-of-Life state machine transition"""
        for record in self:
            if record.lifecycle_stage == 'end_of_life' or record.current_age >= record.expected_lifespan:
                record.end_of_life_plan = 'circular'
                record.circular_market_ready = True
                record.status = 'transitioning'

                # Auto-generate resource listing in Circular Market
                if not record.circular_market_listing_id:
                    record.action_plan_end_of_life()
                
                record.lifecycle_events = (record.lifecycle_events or "") + f"\n{fields.Date.context_today(record)}: AUTOMATED TRANSITION: PRODUCT -> RESOURCE"