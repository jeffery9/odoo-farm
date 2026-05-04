from odoo import models, fields, api


class SeasonalStockForecast(models.Model):
    """
    Dynamic Shelf-life Prediction based on IoT Temperature [US-009-07]
    """
    _name = 'seasonal.stock.forecast'
    _description = 'Seasonal Stock Forecast with Temperature Impact'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Forecast Name', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    season_period = fields.Selection([
        ('q1', 'Q1 - Jan-Mar'),
        ('q2', 'Q2 - Apr-Jun'),
        ('q3', 'Q3 - Jul-Sep'),
        ('q4', 'Q4 - Oct-Dec'),
        ('next_30', 'Next 30 Days'),
        ('next_90', 'Next 90 Days'),
    ], string='Season Period', required=True)

    # Forecast quantities
    base_demand_forecast = fields.Float('Base Demand Forecast')
    temperature_impact_factor = fields.Float('Temperature Impact Factor', default=1.0,
                                           help='Factor by which temperature affects shelf life and demand')
    adjusted_demand_forecast = fields.Float('Adjusted Demand Forecast', compute='_compute_adjusted_forecast', store=True, precompute=True)

    # Temperature data
    avg_temperature = fields.Float('Avg Temperature (℃)')
    temperature_deviation = fields.Float('Temperature Deviation (±℃)')
    humidity_level = fields.Float('Avg Humidity (%)')

    # Shelf life impact
    base_shelf_life_days = fields.Integer('Base Shelf Life (Days)')
    temperature_adjusted_shelf_life = fields.Integer('Temperature-adjusted Shelf Life', compute='_compute_shelf_life', store=True, precompute=True)
    shelf_life_reduction_days = fields.Integer('Shelf Life Reduction (Days)', compute='_compute_shelf_life', store=True, precompute=True)

    # Inventory recommendations
    recommended_safety_stock = fields.Float('Recommended Safety Stock')
    reorder_point = fields.Float('Reorder Point')
    suggested_order_quantity = fields.Float('Suggested Order Quantity', compute='_compute_order_quantity', store=True, precompute=True)

    @api.depends('base_demand_forecast', 'temperature_impact_factor')
    def _compute_adjusted_forecast(self):
        for forecast in self:
            forecast.adjusted_demand_forecast = forecast.base_demand_forecast * forecast.temperature_impact_factor

    @api.depends('base_shelf_life_days', 'temperature_impact_factor', 'avg_temperature')
    def _compute_shelf_life(self):
        for forecast in self:
            # Calculate shelf life reduction based on temperature impact
            if forecast.avg_temperature and forecast.base_shelf_life_days > 0:
                # Higher temperature reduces shelf life
                temp_factor = max(0.1, 2.0 - (forecast.avg_temperature / 25.0))  # Simplified model
                adjusted_life = int(forecast.base_shelf_life_days * temp_factor * forecast.temperature_impact_factor)
                forecast.shelf_life_reduction_days = forecast.base_shelf_life_days - adjusted_life
                forecast.temperature_adjusted_shelf_life = max(1, adjusted_life)
            else:
                forecast.temperature_adjusted_shelf_life = forecast.base_shelf_life_days
                forecast.shelf_life_reduction_days = 0

    @api.depends('adjusted_demand_forecast', 'recommended_safety_stock')
    def _compute_order_quantity(self):
        for forecast in self:
            forecast.suggested_order_quantity = forecast.adjusted_demand_forecast + forecast.recommended_safety_stock

    def action_apply_forecast_to_inventory(self):
        """Apply forecast recommendations to inventory planning"""
        # This would typically integrate with stock level calculations
        pass


class PrecoolingProcess(models.Model):
    """
    Post-harvest Pre-cooling Process Tracking [US-009-08]
    """
    _name = 'precooling.process'
    _description = 'Post-harvest Pre-cooling Process'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Process Reference', required=True, default='/')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    lot_id = fields.Many2one('stock.lot', string='Harvest Lot', required=True)
    batch_number = fields.Char('Batch Number', related='lot_id.name', store=True)

    # Pre-cooling details
    harvest_date = fields.Datetime('Harvest Date', required=True)
    start_precooling_date = fields.Datetime('Start Pre-cooling', default=fields.Datetime.now)
    target_temperature = fields.Float('Target Temperature (℃)', required=True)
    initial_temperature = fields.Float('Initial Temperature (℃)')

    # Process tracking
    current_temperature = fields.Float('Current Temperature (℃)')
    target_humidity = fields.Float('Target Humidity (%)')
    current_humidity = fields.Float('Current Humidity (%)')

    # Time tracking
    cooling_duration_hours = fields.Float('Target Cooling Duration (hours)', required=True)
    actual_cooling_duration = fields.Float('Actual Cooling Duration (hours)', compute='_compute_duration', store=True, precompute=True)
    cooling_progress = fields.Float('Cooling Progress (%)', compute='_compute_progress', store=True, precompute=True)

    # Status
    status = fields.Selection([
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], string='Status', default='pending')

    # Equipment and location
    cooling_equipment_id = fields.Many2one('farm.vehicle', string='Cooling Equipment', domain=[('vehicle_type', '=', 'refrigerated')])
    storage_zone_id = fields.Many2one('cold.storage.zone', string='Storage Zone')

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('precooling.process') or '/'
        return super().create(vals)

    @api.depends('start_precooling_date')
    def _compute_duration(self):
        for process in self:
            if process.start_precooling_date and process.harvest_date:
                duration = (process.start_precooling_date - process.harvest_date).total_seconds() / 3600
                process.actual_cooling_duration = duration
            else:
                process.actual_cooling_duration = 0

    @api.depends('current_temperature', 'target_temperature')
    def _compute_progress(self):
        for process in self:
            if process.target_temperature != 0:
                # Calculate progress as temperature reduction
                temp_reduction_needed = process.initial_temperature - process.target_temperature
                temp_reduction_achieved = process.initial_temperature - (process.current_temperature or process.initial_temperature)
                if temp_reduction_needed != 0:
                    progress = (temp_reduction_achieved / temp_reduction_needed) * 100
                    process.cooling_progress = max(0, min(100, progress))
                else:
                    process.cooling_progress = 100 if process.current_temperature == process.target_temperature else 0
            else:
                process.cooling_progress = 0

    def action_start_precooling(self):
        """Start the pre-cooling process"""
        self.write({
            'status': 'in_progress',
            'start_precooling_date': fields.Datetime.now()
        })

    def action_complete_precooling(self):
        """Complete the pre-cooling process"""
        self.write({
            'status': 'completed',
            'actual_cooling_duration': self.actual_cooling_duration
        })

    def action_failed_precooling(self):
        """Mark pre-cooling as failed"""
        self.write({
            'status': 'failed'
        })