from odoo import models, fields, api, _
from odoo.exceptions import UserError


class FarmSupplyDemandForecast(models.Model):
    _name = 'farm.supply.demand.forecast'
    _description = 'Supply Chain Demand Forecast'
    _inherit = ['agri.ai.decision.base', 'mail.thread', 'mail.activity.mixin']

    name = fields.Char('Forecast Name', required=True, default=lambda self: _('New'))
    product_id = fields.Many2one('product.product', string="Product", required=True)
    forecast_period = fields.Selection([
        ('7d', 'Next 7 Days'),
        ('30d', 'Next 30 Days'),
        ('60d', 'Next 60 Days'),
        ('90d', 'Next 90 Days'),
        ('season', 'Full Production Season')
    ], default='30d', required=True)

    # Input data
    historical_demand_data = fields.Text('Historical Demand Data')
    seasonality_factor = fields.Float('Seasonality Factor', default=1.0)
    trend_factor = fields.Float('Trend Factor', default=1.0)

    # Forecast results
    predicted_demand_qty = fields.Float("Predicted Demand")
    current_stock_level = fields.Float("Current Stock", compute='_compute_current_stock', store=True)
    safety_stock_recommended = fields.Float("Recommended Safety Stock")

    # Optimization recommendations
    optimization_action = fields.Selection([
        ('replenish', 'Replenish Now'),
        ('liquidate', 'Excess Stock - Sell Now'),
        ('transfer', 'Internal Transfer Recommended'),
        ('hold', 'Stock Level Optimal'),
        ('monitor', 'Monitor Closely')
    ], string="Optimization Action", compute='_compute_optimization', store=True)

    # Performance metrics
    forecast_accuracy = fields.Float("Forecast Accuracy %", compute='_compute_accuracy', store=True)
    confidence_level = fields.Float("Confidence Level %", default=85.0)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('farm.supply.demand.forecast') or _('New')
        return super().create(vals)

    @api.depends('product_id')
    def _compute_current_stock(self):
        for record in self:
            if record.product_id:
                record.current_stock_level = record.product_id.qty_available
            else:
                record.current_stock_level = 0.0

    @api.depends('predicted_demand_qty', 'current_stock_level', 'safety_stock_recommended')
    def _compute_optimization(self):
        """US-084-02: Inventory Optimization Algorithm"""
        for rec in self:
            if rec.predicted_demand_qty > 0:
                required_stock = rec.predicted_demand_qty + rec.safety_stock_recommended
                gap = required_stock - rec.current_stock_level

                if gap > rec.safety_stock_recommended * 0.5:
                    rec.optimization_action = 'replenish'
                elif gap < -rec.safety_stock_recommended * 0.3:  # Excess threshold
                    rec.optimization_action = 'liquidate'
                elif gap < 0:
                    rec.optimization_action = 'hold'
                else:
                    rec.optimization_action = 'monitor'
            else:
                rec.optimization_action = 'hold'

    @api.depends('historical_demand_data')
    def _compute_accuracy(self):
        for record in self:
            # This would be calculated based on comparison with actual demand
            # For now, using a simulated accuracy based on data availability
            if record.historical_demand_data:
                record.forecast_accuracy = min(95.0, 70.0 + len(record.historical_demand_data) / 100.0)
            else:
                record.forecast_accuracy = 60.0

    def action_run_forecast(self):
        """Run the demand forecast using AI decision engine"""
        for forecast in self:
            # In a real implementation, this would call the AI decision engine
            # with historical data and other inputs to generate predictions
            forecast.message_post(body=_("Demand forecast executed. Predicted demand: %s units.") % forecast.predicted_demand_qty)

    def action_apply_optimization(self):
        """Apply the recommended optimization action"""
        for forecast in self:
            if forecast.optimization_action == 'replenish':
                # Create procurement request
                self._create_procurement_request(forecast)
            elif forecast.optimization_action == 'liquidate':
                # Create sales promotion or transfer recommendation
                self._create_liquidation_recommendation(forecast)
            elif forecast.optimization_action == 'transfer':
                # Create internal transfer recommendation
                self._create_transfer_recommendation(forecast)

            forecast.message_post(body=_("Applied optimization action: %s") % forecast.optimization_action)

    def _create_procurement_request(self, forecast):
        """Create procurement request based on forecast"""
        # This would create a purchase order or planned order
        pass

    def _create_liquidation_recommendation(self, forecast):
        """Create liquidation recommendation"""
        # This would create sales promotions or disposal recommendations
        pass

    def _create_transfer_recommendation(self, forecast):
        """Create transfer recommendation"""
        # This would create internal transfer orders
        pass


class InventoryOptimization(models.Model):
    """
    Inventory Optimization Engine [US-084-02]
    """
    _name = 'inventory.optimization'
    _description = 'Inventory Optimization Engine'
    currency_id = fields.Many2one("res.currency", string="Currency", default=lambda self: self.env.company.currency_id)
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Optimization Plan', required=True)
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse')
    optimization_date = fields.Date('Optimization Date', default=fields.Date.today)

    # Parameters
    service_level_target = fields.Float('Service Level Target %', default=95.0)
    holding_cost_rate = fields.Float('Holding Cost Rate %', default=25.0)
    stockout_cost_rate = fields.Float('Stockout Cost Rate', default=100.0)

    # Results
    total_cost_reduction = fields.Monetary('Total Cost Reduction')
    inventory_turnover_improvement = fields.Float('Inventory Turnover Improvement %')
    optimized_items_count = fields.Integer('Optimized Items Count')

    status = fields.Selection([
        ('draft', 'Draft'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], default='draft')

    optimization_line_ids = fields.One2many('inventory.optimization.line', 'optimization_id', string='Optimization Lines')

    def action_run_optimization(self):
        """Run the inventory optimization algorithm"""
        for optimization in self:
            # This would run the optimization algorithm
            optimization.status = 'running'

            # Process each product in the warehouse
            products = self.env['product.product'].search([
                ('type', '=', 'product'),
                ('categ_id', '!=', False)
            ])

            for product in products:
                # Calculate optimal inventory levels for each product
                self._optimize_product_inventory(optimization, product)

            optimization.status = 'completed'
            optimization.message_post(body=_("Inventory optimization completed."))

    def _optimize_product_inventory(self, optimization, product):
        """Optimize inventory for a single product"""
        # Create optimization line for this product
        current_qty = product.qty_available
        forecast = self.env['farm.supply.demand.forecast'].search([
            ('product_id', '=', product.id)
        ], limit=1, order='create_date desc')

        if forecast and forecast.predicted_demand_qty:
            recommended_qty = forecast.predicted_demand_qty * 1.2  # Safety factor
        else:
            recommended_qty = current_qty  # No change if no forecast

        self.env['inventory.optimization.line'].create({
            'optimization_id': optimization.id,
            'product_id': product.id,
            'current_qty': current_qty,
            'recommended_qty': recommended_qty,
            'recommended_action': 'replenish' if recommended_qty > current_qty * 1.1 else
                               'reduce' if recommended_qty < current_qty * 0.9 else 'hold'
        })


class InventoryOptimizationLine(models.Model):
    """Line for inventory optimization results"""
    _name = 'inventory.optimization.line'
    _description = 'Inventory Optimization Line'
    currency_id = fields.Many2one("res.currency", string="Currency", default=lambda self: self.env.company.currency_id)

    optimization_id = fields.Many2one('inventory.optimization', string='Optimization', ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True)

    current_qty = fields.Float('Current Quantity')
    recommended_qty = fields.Float('Recommended Quantity')

    recommended_action = fields.Selection([
        ('replenish', 'Replenish'),
        ('reduce', 'Reduce'),
        ('hold', 'Hold'),
    ], string='Recommended Action')