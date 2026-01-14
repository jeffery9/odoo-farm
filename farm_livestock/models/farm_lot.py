from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class FarmLot(models.Model):
    _inherit = 'stock.lot'

    # Livestock specific fields extending the base functionality
    animal_count = fields.Integer("Animal Count", default=1)
    average_weight = fields.Float("Average Weight (kg)", help="Current average weight of individuals in this lot.")

    # 生物阶段 [US-05-04]
    biological_stage = fields.Selection([
        ('born', 'Born/Started'),
        ('growing', 'Growing'),
        ('breeding', 'Breeding'),
        ('lactating', 'Lactating'),
        ('finished', 'Finished'),
        ('harvested', 'Harvested')
    ], string="Biological Stage", default='born')

    # US-03-01: 生长预测与饲喂核销
    start_weight = fields.Float("Initial Weight (kg)")
    current_predicted_weight = fields.Float("Predicted Weight (kg)", compute='_compute_predicted_weight', store=True)
    average_daily_gain = fields.Float("Average Daily Gain (kg/day)", default=0.5)

    active_feeding_bom_id = fields.Many2one('mrp.bom', string="Active Feeding Recipe",
                                           domain="[('type', '=', 'normal'), ('intervention_type', '=', 'feeding')]")

    # Breeding and reproduction management
    breeding_status = fields.Selection([
        ('open', 'Open'),
        ('pregnant', 'Pregnant'),
        ('in_heat', 'In Heat'),
        ('dry', 'Dry Period'),
    ], string='Breeding Status')
    expected_farrowing_date = fields.Date('Expected Farrowing/Calving Date')
    breeding_record_ids = fields.One2many(
        'farm.breeding.record',
        'animal_id',
        string='Breeding Records'
    )
    pedigree_info = fields.Text('Pedigree Information')

    # Health management
    health_status = fields.Selection([
        ('healthy', 'Healthy'),
        ('sick', 'Sick'),
        ('quarantine', 'In Quarantine'),
        ('under_treatment', 'Under Treatment'),
    ], string='Health Status', default='healthy')
    last_vaccination_date = fields.Date('Last Vaccination Date')
    vaccination_schedule = fields.Text('Vaccination Schedule')
    medication_records = fields.Text('Medication Records')
    withdrawal_end_datetime = fields.Datetime('Withdrawal Period End')

    # Individual identification
    ear_tag_number = fields.Char('Ear Tag Number')
    animal_name = fields.Char('Animal Name')
    birth_date = fields.Date('Birth Date')
    sire_id = fields.Many2one('stock.lot', string='Sire')
    dam_id = fields.Many2one('stock.lot', string='Dam')

    # Production parameters (for dairy, egg, etc.)
    milk_yield_avg = fields.Float('Average Milk Yield (L/day)')
    lactation_number = fields.Integer('Lactation Number')
    days_in_milk = fields.Integer('Days in Milk')
    egg_production_rate = fields.Float('Egg Production Rate (%)')

    @api.depends('create_date', 'start_weight', 'average_daily_gain')
    def _compute_predicted_weight(self):
        today = fields.Date.today()
        for lot in self:
            if lot.create_date and lot.biological_stage in ['born', 'growing']:
                days_passed = (today - lot.create_date.date()).days
                lot.current_predicted_weight = lot.start_weight + (days_passed * lot.average_daily_gain)
            else:
                lot.current_predicted_weight = lot.average_weight

    def _cron_daily_feed_depletion(self):
        """ 定时任务：每日自动生成饲喂干预并冲减库存 [US-03-01] """
        Intervention = self.env['mrp.production']
        active_lots = self.search([('biological_stage', 'in', ['born', 'growing']), ('active_feeding_bom_id', '!=', False)])

        for lot in active_lots:
            # 自动创建“已完成”的饲喂干预
            intervention = Intervention.create({
                'product_id': lot.product_id.id,
                'bom_id': lot.active_feeding_bom_id.id,
                'product_qty': lot.animal_count, # 按头数计算
                'intervention_type': 'feeding',
                'lot_producing_id': lot.id,
                'date_start': fields.Datetime.now(),
            })
            intervention.action_confirm()
            # 自动确认完成，触发库存冲减
            intervention.button_mark_done()
            _logger.info("Daily feed depletion recorded for lot %s using BOM %s", lot.name, lot.active_feeding_bom_id.name)

    def action_record_mortality(self, qty, reason, notes=None):
        """ 记录减员并发布审计消息 """
        self.ensure_one()
        if qty <= 0:
            raise UserError(_("Quantity must be positive."))

        body = _("DEATH RECORDED: %s animals decreased. Reason: %s. Notes: %s") % (qty, reason, notes or "")
        self.message_post(body=body)

        # 此处未来可扩展：自动生成库存报废单 (stock.scrap)
        return True

    def action_merge_from(self, source_group):
        """ 将源群组合并到当前群组 """
        self.ensure_one()
        if source_group.product_id != self.product_id:
            raise UserError(_("Cannot merge groups of different products."))

        body = _("MERGE: Group %s has been merged into this group.") % source_group.name
        self.message_post(body=body)

        # 标记源群组为已结束
        source_group.write({'biological_stage': 'harvested', 'active': False})
        return True

    def action_update_health_status(self):
        """Action to update health status"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'farm.animal.health.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': False,
            'target': 'new',
            'context': {
                'default_animal_id': self.id,
                'default_health_status': self.health_status,
            },
            'name': 'Update Health Status',
        }

    def action_record_breeding(self):
        """Action to record breeding event"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'farm.breeding.record',
            'view_mode': 'form',
            'res_id': False,
            'target': 'new',
            'context': {
                'default_animal_id': self.id,
                'default_breeding_date': fields.Date.today(),
            },
            'name': 'Record Breeding Event',
        }

    def action_calculate_expected_yield(self):
        """Calculate expected milk/egg yield based on animal characteristics"""
        for animal in self:
            if animal.biological_stage == 'lactating':
                # Calculate expected milk yield based on lactation number and days in milk
                base_yield = 20.0  # base yield in liters
                adjustment = min(animal.lactation_number * 0.5, 3.0)  # yield increases with lactation
                day_factor = max(1.0 - (animal.days_in_milk / 500), 0.7)  # yield decreases as days in milk increases
                animal.milk_yield_avg = base_yield + adjustment if animal.lactation_number > 0 else base_yield * day_factor


class FarmBreedingRecord(models.Model):
    """
    Breeding record model to track reproduction events in livestock
    """
    _name = 'farm.breeding.record'
    _description = 'Farm Breeding Record'
    _order = 'breeding_date desc'

    animal_id = fields.Many2one(
        'stock.lot',
        string='Animal',
        required=True,
        domain=[('is_animal', '=', True)]
    )
    breeding_date = fields.Date('Breeding Date', required=True, default=fields.Date.today)
    breeding_method = fields.Selection([
        ('natural', 'Natural Mating'),
        ('artificial', 'Artificial Insemination'),
        ('embryo_transfer', 'Embryo Transfer'),
    ], string='Breeding Method', default='natural')
    sire_id = fields.Many2one(
        'stock.lot',
        string='Sire Used',
        domain=[('is_animal', '=', True), ('breeding_status', '=', 'open')]
    )
    gestation_days = fields.Integer('Expected Gestation Days')
    expected_offspring_count = fields.Integer('Expected Offspring Count', default=1)
    breeding_notes = fields.Text('Breeding Notes')
    pregnancy_test_date = fields.Date('Pregnancy Test Date')
    pregnancy_test_result = fields.Boolean('Pregnancy Test Result')

    # Offspring tracking
    offspring_ids = fields.One2many(
        'stock.lot',
        'dam_id',
        string='Offspring'
    )

    @api.onchange('sire_id')
    def _onchange_sire_id(self):
        """Set expected gestation days based on sire species"""
        if self.sire_id:
            # Set default gestation period based on species
            species = self.sire_id.product_id.name
            if 'pig' in species.lower():
                self.gestation_days = 114
            elif 'cow' in species.lower() or 'cattle' in species.lower():
                self.gestation_days = 283
            elif 'sheep' in species.lower():
                self.gestation_days = 150
            elif 'goat' in species.lower():
                self.gestation_days = 150
            elif 'horse' in species.lower():
                self.gestation_days = 340


class FarmAnimalHealthWizard(models.TransientModel):
    """
    Wizard model to update animal health status
    """
    _name = 'farm.animal.health.wizard'
    _description = 'Farm Animal Health Update Wizard'

    animal_id = fields.Many2one(
        'stock.lot',
        string='Animal',
        required=True
    )
    health_status = fields.Selection([
        ('healthy', 'Healthy'),
        ('sick', 'Sick'),
        ('quarantine', 'In Quarantine'),
        ('under_treatment', 'Under Treatment'),
    ], string='Health Status', required=True)
    treatment_notes = fields.Text('Treatment Notes')
    next_vaccination_date = fields.Date('Next Vaccination Date')

    def action_update_health_status(self):
        """Update the animal's health status"""
        self.ensure_one()
        self.animal_id.write({
            'health_status': self.health_status,
            'medication_records': self.treatment_notes,
            'last_vaccination_date': self.next_vaccination_date,
        })
        return {'type': 'ir.actions.act_window_close'}