from odoo import models, fields, api


class OrchardOperation(models.Model):
    """
    Orchard Operation model to manage fruit tree and perennial crop operations
    """
    _name = 'farm.orchard.operation'
    _description = 'Orchard Operation'
    _inherits = {'project.task': 'operation_id'}
    _inherit = ['mail.thread', 'mail.activity.mixin']

    operation_id = fields.Many2one(
        'project.task',
        required=True,
        ondelete='cascade',
        string='Operation Task'
    )

    # Orchard specific fields
    tree_id = fields.Many2one(
        'stock.lot',
        domain=[('is_fruit_tree', '=', True)],
        string='Fruit Tree',
        help='Specific fruit tree for this operation'
    )
    tree_age = fields.Integer(
        string='Tree Age (years)',
        related='tree_id.tree_age',
        store=True,
        readonly=True
    )
    tree_variety = fields.Char(
        string='Tree Variety',
        related='tree_id.tree_variety',
        readonly=True
    )
    flowering_start_date = fields.Date(string='Flowering Start Date')
    flowering_end_date = fields.Date(string='Flowering End Date')
    expected_fruit_count = fields.Integer(string='Expected Fruit Count')
    pruning_type = fields.Selection([
        ('formative', 'Formative Pruning'),
        ('maintenance', 'Maintenance Pruning'),
        ('fruiting', 'Fruiting Pruning'),
        ('rejuvenation', 'Rejuvenation Pruning'),
    ], string='Pruning Type')
    training_system = fields.Selection([
        ('central_leader', 'Central Leader'),
        ('open_center', 'Open Center'),
        ('vase_shaped', 'Vase Shaped'),
        ('trellis', 'Trellis System'),
        (' espalier', 'Espalier'),
    ], string='Training System')

    # Orchard management
    irrigation_method = fields.Selection([
        ('drip', 'Drip Irrigation'),
        ('micro_sprinkler', 'Micro Sprinkler'),
        ('flood', 'Flood Irrigation'),
        ('furrow', 'Furrow Irrigation'),
    ], string='Irrigation Method')

    canopy_height = fields.Float(string='Canopy Height (m)')
    canopy_spread = fields.Float(string='Canopy Spread (m)')

    # Linked to specific orchard areas
    orchard_block_id = fields.Many2one(
        'stock.location',
        domain=[('is_orchard_block', '=', True)],
        string='Orchard Block',
        help='Specific orchard block or section'
    )
    rootstock_id = fields.Many2one(
        'product.product',
        domain=[('is_rootstock', '=', True)],
        string='Rootstock',
        help='Rootstock variety used'
    )
    pollinator_tree_ids = fields.Many2many(
        'stock.lot',
        'orchard_pollinator_rel',
        'operation_id', 'tree_id',
        domain=[('is_fruit_tree', '=', True)],
        string='Pollinator Trees',
        help='Trees that serve as pollinators for this operation'
    )

    # Lifecycle and seasonal management
    dormant_treatment = fields.Text(string='Dormant Season Treatment')
    growing_season_notes = fields.Text(string='Growing Season Notes')
    harvest_readiness_check = fields.Boolean(string='Harvest Readiness Check')
    fruit_quality_grade = fields.Selection([
        ('grade_a', 'Grade A'),
        ('grade_b', 'Grade B'),
        ('grade_c', 'Grade C'),
    ], string='Fruit Quality Grade')

    @api.onchange('tree_id')
    def _onchange_tree_id(self):
        """Update related fields when tree is selected"""
        if self.tree_id:
            self.orchard_block_id = self.tree_id.location_id
            self.tree_age = self.tree_id.tree_age
            self.tree_variety = self.tree_id.tree_variety

    def action_view_tree_details(self):
        """Action to view detailed tree information"""
        self.ensure_one()
        if self.tree_id:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'stock.lot',
                'res_id': self.tree_id.id,
                'view_mode': 'form',
                'target': 'current',
            }
        return {'type': 'ir.actions.act_window.close'}


class FruitTree(models.Model):
    """
    Fruit Tree model to manage individual trees in orchards
    """
    _name = 'stock.lot'  # Inherit from stock.lot to leverage existing functionality
    _inherit = 'stock.lot'

    # Orchard specific fields for trees
    is_fruit_tree = fields.Boolean(string='Is Fruit Tree', default=False)
    tree_age = fields.Integer(string='Tree Age (years)')
    tree_variety = fields.Char(string='Tree Variety')
    planting_date = fields.Date(string='Planting Date')
    rootstock_variety = fields.Char(string='Rootstock Variety')
    training_system = fields.Selection([
        ('central_leader', 'Central Leader'),
        ('open_center', 'Open Center'),
        ('vase_shaped', 'Vase Shaped'),
        ('trellis', 'Trellis System'),
        ('espalier', 'Espalier'),
    ], string='Training System')

    # Production information
    last_pruning_date = fields.Date(string='Last Pruning Date')
    last_fruit_harvest = fields.Date(string='Last Fruit Harvest')
    annual_yield_history = fields.Text(string='Annual Yield History')

    # Physical characteristics
    canopy_height = fields.Float(string='Canopy Height (m)')
    canopy_spread = fields.Float(string='Canopy Spread (m)')
    trunk_diameter = fields.Float(string='Trunk Diameter (cm)')

    # Lifecycle
    expected_lifespan = fields.Integer(string='Expected Lifespan (years)')
    productive_years = fields.Integer(string='Productive Years')

    # Special attributes
    is_pollinator = fields.Boolean(string='Is Pollinator Tree')
    compatible_varieties = fields.Text(string='Compatible Varieties for Pollination')

    # US-34-01 & US-34-02: Advanced Perennial Asset Management
    productive_state = fields.Selection([
        ('juvenile', 'Juvenile (Non-bearing)'),
        ('ascending', 'Early Bearing'),
        ('peak', 'Peak Production'),
        ('declining', 'Declining Yield'),
        ('dead', 'Dead/Removed')
    ], string="Productive State", default='juvenile')
    
    yield_record_ids = fields.One2many('farm.plant.yield.record', 'lot_id', string="Yield History")
    total_cumulative_yield = fields.Float("Cumulative Yield (kg)", compute='_compute_cumulative_yield', store=True)

    @api.depends('yield_record_ids.quantity')
    def _compute_cumulative_yield(self):
        for lot in self:
            lot.total_cumulative_yield = sum(lot.yield_record_ids.mapped('quantity'))

class PlantYieldRecord(models.Model):
    """ US-34-02: Records historical yield for a specific plant asset """
    _name = 'farm.plant.yield.record'
    _description = 'Plant Yield Record'
    _order = 'harvest_date desc'

    lot_id = fields.Many2one('stock.lot', string="Plant Asset", required=True, ondelete='cascade')
    harvest_date = fields.Date("Harvest Date", default=fields.Date.today)
    quantity = fields.Float("Yield Quantity (kg)", required=True)
    quality_grade = fields.Selection([
        ('a', 'Grade A'), ('b', 'Grade B'), ('c', 'Grade C')
    ], string="Quality Grade")
    campaign_id = fields.Many2one('agricultural.campaign', string="Campaign/Season")