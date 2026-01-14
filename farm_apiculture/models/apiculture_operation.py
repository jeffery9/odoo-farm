from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class FarmApicultureOperation(models.Model):
    """
    Apiculture operation model for managing bee colonies, hives, honey production, and nectar tracking
    """
    _name = 'farm.apiculture.operation'
    _description = 'Farm Apiculture Operation'
    _inherit = 'project.task'  # Inherit from project.task to leverage existing task functionality

    # Hive and Colony Management
    hive_id = fields.Many2one('stock.lot', string='Hive',
                              domain=[('product_id.categ_id.name', 'ilike', 'hive')])
    hive_location = fields.Char('Hive Location')
    colony_strength = fields.Selection([
        ('weak', 'Weak'),
        ('moderate', 'Moderate'),
        ('strong', 'Strong'),
        ('very_strong', 'Very Strong'),
    ], string='Colony Strength', default='moderate')
    queen_status = fields.Selection([
        ('good', 'Good'),
        ('poor', 'Poor'),
        ('queenless', 'Queenless'),
        ('new_queen', 'New Queen'),
    ], string='Queen Status', default='good')
    queen_age_months = fields.Integer('Queen Age (months)')
    colony_population = fields.Integer('Colony Population (bees)')

    # Bee Species and Breeds
    bee_species = fields.Char('Bee Species')
    bee_breed = fields.Char('Bee Breed')

    # Nectar Source Management
    nectar_sources = fields.Text('Nectar Sources', help='List of available nectar sources')
    flowering_plants = fields.Text('Flowering Plants in Range')
    nectar_availability = fields.Selection([
        ('abundant', 'Abundant'),
        ('moderate', 'Moderate'),
        ('scarce', 'Scarce'),
        ('none', 'None'),
    ], string='Nectar Availability', default='moderate')

    # Honey Production
    honey_production_stage = fields.Selection([
        ('foraging', 'Foraging'),
        ('in_hive_processing', 'In-Hive Processing'),
        ('honey_flow', 'Honey Flow'),
        ('harvest_prep', 'Harvest Preparation'),
        ('harvesting', 'Harvesting'),
        ('post_harvest', 'Post Harvest'),
    ], string='Honey Production Stage', default='foraging')
    honey_store_level = fields.Float('Honey Store Level (kg)')
    honey_production_rate = fields.Float('Daily Honey Production (kg/day)')
    last_harvest_date = fields.Date('Last Harvest Date')
    last_harvest_yield = fields.Float('Last Harvest Yield (kg)')

    # Migration and Movement
    migration_schedule = fields.Text('Migration Schedule')
    current_location = fields.Char('Current Location')
    previous_locations = fields.Text('Previous Locations')
    migration_reason = fields.Char('Migration Reason')

    # Bee Health Management
    health_status = fields.Selection([
        ('healthy', 'Healthy'),
        ('sick', 'Sick'),
        ('pest_infested', 'Pest Infested'),
        ('disease_outbreak', 'Disease Outbreak'),
        ('queen_issue', 'Queen Issue'),
    ], string='Health Status', default='healthy')
    health_notes = fields.Text('Health Notes')
    pest_control_used = fields.Char('Pest Control Used')

    # Apiculture specific stages
    apiculture_stage = fields.Selection([
        ('colony_establishment', 'Colony Establishment'),
        ('hive_preparation', 'Hive Preparation'),
        ('colony_inspection', 'Colony Inspection'),
        ('nectar_tracking', 'Nectar Tracking'),
        ('foraging_management', 'Foraging Management'),
        ('honey_production', 'Honey Production'),
        ('colony_reproduction', 'Colony Reproduction'),
        ('swarm_control', 'Swarm Control'),
        ('harvest_planning', 'Harvest Planning'),
        ('harvesting', 'Harvesting'),
        ('post_harvest', 'Post Harvest'),
    ], string='Apiculture Stage', default='colony_establishment')

    # Seasonal Management
    season = fields.Selection([
        ('spring', 'Spring'),
        ('summer', 'Summer'),
        ('fall', 'Fall'),
        ('winter', 'Winter'),
    ], string='Season', default='spring')

    # Breeding and Reproduction
    breeding_status = fields.Selection([
        ('not_breeding', 'Not Breeding'),
        ('breeding', 'Breeding'),
        ('swarming_likely', 'Swarming Likely'),
        ('swarmed', 'Swarmed'),
    ], string='Breeding Status', default='not_breeding')
    swarm_date = fields.Date('Swarm Date')
    swarm_details = fields.Text('Swarm Details')

    @api.depends('honey_production_rate', 'colony_strength')
    def _compute_honey_store_level(self):
        """Compute honey store level based on production rate and colony strength"""
        for record in self:
            # This would be calculated based on actual production data
            if record.honey_production_rate > 0:
                record.honey_store_level = record.honey_store_level or 0  # In reality, would track over time

    def action_update_colony_population(self, population):
        """Update colony population"""
        self.ensure_one()
        self.write({'colony_population': population})
        self.message_post(body=_("Colony population updated to: %s bees") % population)
        return True

    def action_record_harvest(self, yield_amount, quality_grade=None):
        """Record honey harvest"""
        self.ensure_one()
        self.write({
            'last_harvest_date': fields.Date.today(),
            'last_harvest_yield': yield_amount,
        })

        body = _("HONEY HARVEST RECORDED: %s kg harvested on %s") % (yield_amount, fields.Date.today())
        if quality_grade:
            body += f" Quality: {quality_grade}"
        self.message_post(body=body)
        return True

    def action_update_health_status(self, status, notes=None):
        """Update bee health status"""
        self.ensure_one()
        self.write({
            'health_status': status,
            'health_notes': notes
        })

        body = _("HEALTH STATUS UPDATE: %s. %s") % (status, notes or "")
        self.message_post(body=body)
        return True

    def action_schedule_migration(self, destination, reason, departure_date):
        """Schedule hive migration"""
        self.ensure_one()
        self.write({
            'migration_schedule': f"Moving to {destination} on {departure_date} for {reason}",
            'current_location': destination,
            'migration_reason': reason,
        })

        body = _("HIVE MIGRATION SCHEDULED: To %s on %s for %s") % (destination, departure_date, reason)
        self.message_post(body=body)
        return True

    def action_add_location_history(self, location):
        """Add location to history"""
        self.ensure_one()
        current_history = self.previous_locations or ""
        new_entry = f"{fields.Datetime.now()}: Moved to {location}\n"
        self.write({'previous_locations': current_history + new_entry})
        return True

    def action_record_swarm(self, swarm_details=None):
        """Record swarm event"""
        self.ensure_one()
        self.write({
            'breeding_status': 'swarmed',
            'swarm_date': fields.Date.today(),
            'swarm_details': swarm_details,
        })

        body = _("SWARM RECORDED: On %s. %s") % (fields.Date.today(), swarm_details or "")
        self.message_post(body=body)
        return True

    def action_check_colony(self):
        """Perform colony inspection"""
        self.ensure_one()
        # This would typically update various colony metrics based on inspection
        self.message_post(body=_("Colony inspection performed on %s") % fields.Date.today())
        return True


class FarmHiveInspection(models.Model):
    """
    Hive inspection model for tracking regular inspections and health checks
    """
    _name = 'farm.hive.inspection'
    _description = 'Farm Hive Inspection'
    _order = 'inspection_date desc'

    operation_id = fields.Many2one('farm.apiculture.operation', string='Apiculture Operation', required=True)
    inspection_date = fields.Date('Inspection Date', default=fields.Date.today, required=True)
    inspector = fields.Char('Inspector')

    # Inspection results
    colony_strength = fields.Selection([
        ('weak', 'Weak'),
        ('moderate', 'Moderate'),
        ('strong', 'Strong'),
        ('very_strong', 'Very Strong'),
    ], string='Colony Strength')
    queen_status = fields.Selection([
        ('good', 'Good'),
        ('poor', 'Poor'),
        ('queenless', 'Queenless'),
        ('new_queen', 'New Queen'),
    ], string='Queen Status')
    honey_store_level = fields.Float('Honey Store Level (kg)')
    bee_population = fields.Integer('Bee Population')

    # Health and issues
    health_status = fields.Selection([
        ('healthy', 'Healthy'),
        ('sick', 'Sick'),
        ('pest_infested', 'Pest Infested'),
        ('disease_outbreak', 'Disease Outbreak'),
    ], string='Health Status')
    issues_found = fields.Text('Issues Found')
    recommendations = fields.Text('Recommendations')

    # Actions taken
    actions_taken = fields.Text('Actions Taken')
    next_inspection_date = fields.Date('Next Inspection Date')

    @api.model
    def create(self, vals):
        """Override create to update operation with current values"""
        record = super().create(vals)
        if record.operation_id:
            # Update the current values in the operation
            updates = {}
            if record.colony_strength:
                updates['colony_strength'] = record.colony_strength
            if record.queen_status:
                updates['queen_status'] = record.queen_status
            if record.honey_store_level:
                updates['honey_store_level'] = record.honey_store_level
            if record.bee_population:
                updates['colony_population'] = record.bee_population
            if record.health_status:
                updates['health_status'] = record.health_status
            if updates:
                record.operation_id.write(updates)
        return record