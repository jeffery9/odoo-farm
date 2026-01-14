from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class FarmMushroomOperation(models.Model):
    """
    Mushroom operation model for managing cultivation, environmental control, and harvest tracking
    """
    _name = 'farm.mushroom.operation'
    _description = 'Farm Mushroom Operation'
    _inherit = 'project.task'  # Inherit from project.task to leverage existing task functionality

    # Mushroom Strain and Spawn Management
    mushroom_strain = fields.Char('Mushroom Strain', help='Specific strain of mushroom being cultivated')
    spawn_type = fields.Selection([
        ('grain_spawn', 'Grain Spawn'),
        ('sawdust_spawn', 'Sawdust Spawn'),
        ('plug_spawn', 'Plug Spawn'),
        ('liquid_spawn', 'Liquid Spawn'),
    ], string='Spawn Type', default='grain_spawn')
    spawn_source = fields.Char('Spawn Source')
    spawn_date = fields.Date('Spawn Date')

    # Substrate Management
    substrate_type = fields.Char('Substrate Type', help='Type of growing medium used')
    substrate_recipe = fields.Text('Substrate Recipe')
    substrate_preparation_date = fields.Date('Substrate Preparation Date')
    substrate_sterilization_temp = fields.Float('Sterilization Temperature (°C)')
    substrate_sterilization_time = fields.Float('Sterilization Time (hours)')

    # Environmental Control
    growing_temperature = fields.Float('Growing Temperature (°C)')
    humidity_level = fields.Float('Humidity Level (%)')
    co2_level = fields.Float('CO2 Level (ppm)')
    ventilation_rate = fields.Float('Ventilation Rate (m³/hour)')
    light_intensity = fields.Float('Light Intensity (lux)')

    # Mushroom specific stages
    mushroom_stage = fields.Selection([
        ('strain_selection', 'Strain Selection'),
        ('substrate_preparation', 'Substrate Preparation'),
        ('sterilization', 'Sterilization'),
        ('inoculation', 'Inoculation'),
        ('colonization', 'Colonization'),
        ('fruiting_induction', 'Fruiting Induction'),
        ('flushing', 'Flushing/Harvesting'),
        ('harvesting', 'Harvesting'),
        ('post_harvest', 'Post Harvest'),
    ], string='Mushroom Stage', default='strain_selection')

    # Growth Tracking
    colonization_date = fields.Date('Colonization Date')
    first_fruiting_date = fields.Date('First Fruiting Date')
    flush_count = fields.Integer('Flush Count', help='Number of harvest rounds from same substrate')
    current_flush_number = fields.Integer('Current Flush Number')
    days_to_first_flush = fields.Integer('Days to First Flush', compute='_compute_growth_metrics', store=True)

    # Harvest Management
    harvest_schedule_ids = fields.One2many('farm.mushroom.harvest', 'operation_id', string='Harvest Schedule')
    total_yield = fields.Float('Total Yield (kg)', compute='_compute_total_yield', store=True)
    average_yield_per_flush = fields.Float('Avg Yield per Flush (kg)', compute='_compute_average_yield', store=True)

    # Quality Control
    contamination_status = fields.Selection([
        ('clean', 'Clean'),
        ('contaminated', 'Contaminated'),
        ('partially_contaminated', 'Partially Contaminated'),
        ('cleared', 'Cleared'),
    ], string='Contamination Status', default='clean')
    contamination_notes = fields.Text('Contamination Notes')

    # Batch Management
    batch_number = fields.Char('Batch Number', default=lambda self: self._generate_batch_number())
    batch_size = fields.Float('Batch Size', help='Amount of substrate or fruiting blocks')

    @api.model
    def _generate_batch_number(self):
        """Generate a unique batch number"""
        return self.env['ir.sequence'].next_by_code('mushroom.batch') or 'MUSH-BATCH-001'

    @api.depends('first_fruiting_date', 'spawn_date')
    def _compute_growth_metrics(self):
        """Compute growth-related metrics"""
        for record in self:
            if record.first_fruiting_date and record.spawn_date:
                from datetime import datetime
                spawn_dt = fields.Date.from_string(record.spawn_date)
                fruiting_dt = fields.Date.from_string(record.first_fruiting_date)
                record.days_to_first_flush = (fruiting_dt - spawn_dt).days
            else:
                record.days_to_first_flush = 0

    @api.depends('harvest_schedule_ids')
    def _compute_total_yield(self):
        """Compute total yield from all harvests"""
        for record in self:
            record.total_yield = sum(harvest.yield_amount for harvest in record.harvest_schedule_ids)

    @api.depends('total_yield', 'flush_count')
    def _compute_average_yield(self):
        """Compute average yield per flush"""
        for record in self:
            if record.flush_count > 0:
                record.average_yield_per_flush = record.total_yield / record.flush_count
            else:
                record.average_yield_per_flush = 0.0

    def action_add_contamination_note(self, note):
        """Add contamination note"""
        self.ensure_one()
        current_notes = self.contamination_notes or ""
        new_note = f"{fields.Datetime.now()}: {note}\n"
        self.write({'contamination_notes': current_notes + new_note})
        return True

    def action_update_contamination_status(self, status):
        """Update contamination status"""
        self.ensure_one()
        self.write({'contamination_status': status})
        self.message_post(body=_("Contamination status updated to: %s") % status)
        return True

    def action_record_flush(self, flush_number, yield_amount, notes=None):
        """Record a flush/harvest event"""
        self.ensure_one()

        harvest = self.env['farm.mushroom.harvest'].create({
            'operation_id': self.id,
            'flush_number': flush_number,
            'yield_amount': yield_amount,
            'harvest_date': fields.Date.today(),
            'notes': notes,
        })

        # Update flush count if this is a new flush
        if flush_number > self.flush_count:
            self.flush_count = flush_number

        # Update current flush
        self.current_flush_number = flush_number

        body = _("FLUSH RECORDED: Flush #%s, Yield: %s kg. %s") % (
            flush_number, yield_amount, notes or "")
        self.message_post(body=body)
        return harvest

    def action_start_colonization(self):
        """Start colonization phase"""
        self.ensure_one()
        self.write({
            'mushroom_stage': 'colonization',
            'colonization_date': fields.Date.today()
        })
        self.message_post(body=_("Colonization started on %s") % fields.Date.today())
        return True

    def action_start_fruiting(self):
        """Start fruiting induction"""
        self.ensure_one()
        self.write({
            'mushroom_stage': 'fruiting_induction',
            'first_fruiting_date': fields.Date.today()
        })
        self.message_post(body=_("Fruiting induction started on %s") % fields.Date.today())
        return True


class FarmMushroomHarvest(models.Model):
    """
    Mushroom harvest model for tracking multiple harvests from same substrate
    """
    _name = 'farm.mushroom.harvest'
    _description = 'Farm Mushroom Harvest'
    _order = 'harvest_date desc, flush_number asc'

    operation_id = fields.Many2one('farm.mushroom.operation', string='Operation', required=True)
    flush_number = fields.Integer('Flush Number', required=True, help='Harvest round from same substrate')
    harvest_date = fields.Date('Harvest Date', default=fields.Date.today, required=True)
    yield_amount = fields.Float('Yield Amount (kg)', required=True)
    notes = fields.Text('Harvest Notes')
    quality_grade = fields.Selection([
        ('premium', 'Premium'),
        ('standard', 'Standard'),
        ('substandard', 'Substandard'),
    ], string='Quality Grade')

    def action_update_quality_grade(self, grade):
        """Update quality grade for this harvest"""
        self.ensure_one()
        self.write({'quality_grade': grade})
        return True