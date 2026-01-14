from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class FarmAquacultureOperation(models.Model):
    """
    Aquaculture operation model for managing pond/tank operations, water quality, feeding, and growth tracking
    """
    _name = 'farm.aquaculture.operation'
    _description = 'Farm Aquaculture Operation'
    _inherit = 'project.task'  # Inherit from project.task to leverage existing task functionality

    # Pond/Tank Information
    pond_id = fields.Many2one('stock.lot', string='Pond/Tank',
                              domain=[('product_id.categ_id.name', 'ilike', 'pond')])
    pond_capacity = fields.Float('Pond Capacity (m³)', related='pond_id.volume', store=True)
    aquatic_species = fields.Char('Aquatic Species', help='Species name for pond')
    initial_stocking = fields.Integer('Initial Stocking Count')
    current_count = fields.Integer('Current Count', compute='_compute_current_count', store=True)

    # Water Quality Management
    water_temperature = fields.Float('Water Temperature (°C)')
    ph_level = fields.Float('pH Level')
    dissolved_oxygen = fields.Float('Dissolved Oxygen (mg/L)')
    ammonia_level = fields.Float('Ammonia Level (mg/L)')
    nitrite_level = fields.Float('Nitrite Level (mg/L)')
    water_quality_status = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('critical', 'Critical'),
    ], string='Water Quality Status', compute='_compute_water_quality_status', store=True)

    # Feeding Management
    feeding_schedule = fields.Text('Feeding Schedule')
    last_feeding_date = fields.Datetime('Last Feeding Time')
    daily_feeding_rate = fields.Float('Daily Feeding Rate (%)', help='Percentage of body weight fed daily')

    # Growth Tracking
    avg_initial_weight = fields.Float('Avg Initial Weight (g)')
    avg_current_weight = fields.Float('Avg Current Weight (g)', compute='_compute_avg_current_weight', store=True)
    growth_rate = fields.Float('Growth Rate (g/day)', compute='_compute_growth_rate', store=True)
    target_weight = fields.Float('Target Weight (g)')

    # Harvest Management
    harvest_readiness = fields.Boolean('Harvest Readiness', compute='_compute_harvest_readiness', store=True)
    harvest_plan_date = fields.Date('Planned Harvest Date')

    # Aquaculture specific stages
    aquaculture_stage = fields.Selection([
        ('tank_preparation', 'Tank Preparation'),
        ('water_conditioning', 'Water Conditioning'),
        ('seed_stocking', 'Seed Stocking'),
        ('growing', 'Growing'),
        ('harvesting', 'Harvesting'),
        ('post_harvest', 'Post-Harvest'),
    ], string='Aquaculture Stage', default='tank_preparation')

    # Water treatment and circulation
    water_treatment_method = fields.Selection([
        ('mechanical', 'Mechanical'),
        ('biological', 'Biological'),
        ('chemical', 'Chemical'),
        ('uv', 'UV Sterilization'),
        ('ozone', 'Ozone Treatment'),
    ], string='Water Treatment Method')
    circulation_rate = fields.Float('Water Circulation Rate (m³/hour)')

    @api.depends('initial_stocking', 'action_record_mortality', 'action_add_stock')
    def _compute_current_count(self):
        """Compute current stock count"""
        for record in self:
            # This would be calculated based on actual stock movements
            record.current_count = record.initial_stocking if record.initial_stocking else 0

    @api.depends('water_temperature', 'ph_level', 'dissolved_oxygen', 'ammonia_level', 'nitrite_level')
    def _compute_water_quality_status(self):
        """Compute water quality status based on parameters"""
        for record in self:
            # Critical if any parameter is out of normal range
            if (record.dissolved_oxygen < 3.0 or  # Critical low oxygen
                record.ammonia_level > 2.0 or     # Critical high ammonia
                record.ph_level < 6.0 or record.ph_level > 9.0):  # Extreme pH
                record.water_quality_status = 'critical'
            elif (record.dissolved_oxygen < 5.0 or  # Low oxygen
                  record.ammonia_level > 1.0 or    # High ammonia
                  record.ph_level < 6.5 or record.ph_level > 8.5):  # Outside optimal range
                record.water_quality_status = 'poor'
            elif (record.dissolved_oxygen < 6.0 or  # Slightly low oxygen
                  record.ammonia_level > 0.5 or    # Moderate ammonia
                  record.ph_level < 7.0 or record.ph_level > 8.0):  # Not ideal
                record.water_quality_status = 'fair'
            else:
                record.water_quality_status = 'good'

    @api.depends('avg_initial_weight', 'current_count')
    def _compute_avg_current_weight(self):
        """Compute current average weight"""
        for record in self:
            # Simplified calculation - in reality would track individual fish weights
            record.avg_current_weight = record.avg_initial_weight if record.avg_initial_weight else 0

    @api.depends('avg_initial_weight', 'avg_current_weight')
    def _compute_growth_rate(self):
        """Compute growth rate"""
        for record in self:
            # Would need time tracking to calculate actual growth rate
            if record.avg_initial_weight > 0:
                record.growth_rate = (record.avg_current_weight - record.avg_initial_weight) / 1.0  # Placeholder for time calculation
            else:
                record.growth_rate = 0.0

    @api.depends('avg_current_weight', 'target_weight', 'aquaculture_stage')
    def _compute_harvest_readiness(self):
        """Compute if the aquatic species is ready for harvest"""
        for record in self:
            record.harvest_readiness = (record.avg_current_weight >= record.target_weight and
                                      record.aquaculture_stage == 'growing')

    def action_add_stock(self, count, species_type=None):
        """Add stock to pond"""
        self.ensure_one()
        new_count = self.current_count + count
        self.write({'current_count': new_count})

        body = _("ADDITIONAL STOCK: %s new %s added. Total count now: %s") % (count, species_type or "species", new_count)
        self.message_post(body=body)
        return True

    def action_record_mortality(self, count, cause=None):
        """Record mortality"""
        self.ensure_one()
        new_count = max(0, self.current_count - count)
        self.write({'current_count': new_count})

        body = _("MORTALITY RECORDED: %s %s died. Total count now: %s. Cause: %s") % (
            count, self.aquatic_species or "species", new_count, cause or "Unknown")
        self.message_post(body=body)
        return True

    def action_record_water_quality(self, temperature=None, ph=None, dissolved_oxygen=None, ammonia=None, nitrite=None):
        """Record water quality parameters"""
        self.ensure_one()
        updates = {}
        if temperature is not None:
            updates['water_temperature'] = temperature
        if ph is not None:
            updates['ph_level'] = ph
        if dissolved_oxygen is not None:
            updates['dissolved_oxygen'] = dissolved_oxygen
        if ammonia is not None:
            updates['ammonia_level'] = ammonia
        if nitrite is not None:
            updates['nitrite_level'] = nitrite

        if updates:
            self.write(updates)

            body = _("WATER QUALITY UPDATE:\n")
            if temperature: body += f"Temperature: {temperature}°C\n"
            if ph: body += f"pH: {ph}\n"
            if dissolved_oxygen: body += f"Dissolved Oxygen: {dissolved_oxygen} mg/L\n"
            if ammonia: body += f"Ammonia: {ammonia} mg/L\n"
            if nitrite: body += f"Nitrite: {nitrite} mg/L\n"

            self.message_post(body=body)
        return True

    def action_schedule_harvest(self, harvest_date):
        """Schedule harvest"""
        self.ensure_one()
        self.write({'harvest_plan_date': harvest_date})
        self.message_post(body=_("Harvest scheduled for %s") % harvest_date)
        return True


class FarmWaterQualityLog(models.Model):
    """
    Water quality log model for tracking historical water parameters
    """
    _name = 'farm.water.quality.log'
    _description = 'Farm Water Quality Log'
    _order = 'log_date desc'

    operation_id = fields.Many2one('farm.aquaculture.operation', string='Aquaculture Operation', required=True)
    log_date = fields.Datetime('Log Date', default=fields.Datetime.now, required=True)
    temperature = fields.Float('Temperature (°C)')
    ph_level = fields.Float('pH Level')
    dissolved_oxygen = fields.Float('Dissolved Oxygen (mg/L)')
    ammonia_level = fields.Float('Ammonia Level (mg/L)')
    nitrite_level = fields.Float('Nitrite Level (mg/L)')
    water_turbidity = fields.Float('Turbidity (NTU)')
    water_salinity = fields.Float('Salinity (ppt)')
    weather_conditions = fields.Char('Weather Conditions')
    notes = fields.Text('Notes')

    @api.model
    def create(self, vals):
        """Override create to update operation with current values"""
        record = super().create(vals)
        if record.operation_id:
            # Update the current values in the operation
            record.operation_id.write({
                'water_temperature': record.temperature,
                'ph_level': record.ph_level,
                'dissolved_oxygen': record.dissolved_oxygen,
                'ammonia_level': record.ammonia_level,
                'nitrite_level': record.nitrite_level,
            })
        return record