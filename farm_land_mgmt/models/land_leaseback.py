from odoo import models, fields, api, _

class AgriLocation(models.Model):
    _inherit = 'farm.location'

    lease_contract_id = fields.Many2one('farm.land.lease', string="Active Lease Contract")
    is_consolidated = fields.Boolean("Consolidated into Mega-Field", default=False)
    mega_field_id = fields.Many2one('farm.location', string="Parent Mega-Field")

class FarmLandLease(models.Model):
    _name = 'farm.land.lease'
    _description = 'Land Leaseback Contract'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Contract Ref", required=True)
    farmer_id = fields.Many2one('res.partner', string="Lessor (Farmer)", required=True)
    operator_id = fields.Many2one('res.partner', string="Lessee (Operator)", required=True)
    
<<<<<<< HEAD
    land_parcel_ids = fields.Many2many('farm.location', 'farm_land_lease_farm_location_rel', 'lease_id', 'location_id', string="Leased Parcels")
=======
    land_parcel_ids = fields.Many2many('farm.location', 'farm_land_lease_farm_loc_rel', 'lease_id', 'location_id', string="Leased Parcels")
>>>>>>> 5351cad217860264bdd3ca8394fa45a799fce3d0
    total_area = fields.Float("Total Area (mu/ha)", compute="_compute_area", store=True)
    
    start_date = fields.Date("Start Date", required=True)
    end_date = fields.Date("End Date", required=True)
    annual_rent = fields.Float("Annual Rent ($)")
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expired', 'Expired')
    ], default='draft', tracking=True)

    #@api.depends('land_parcel_ids.area')
    def _compute_area(self):
        for contract in self:
            # Assuming area field exists on farm.location from base agri_location
            if hasattr(contract.env['farm.location'], 'area'):
                contract.total_area = sum(contract.land_parcel_ids.mapped('area'))
            else:
                contract.total_area = len(contract.land_parcel_ids) * 1.0 # Mock

    def action_activate(self):
        """
        [US-SCENARIO-28] Digital Land Rights & Leaseback Management
        Activates the lease. Marks parcels as leased and optionally consolidates them.
        """
        for contract in self:
            contract.state = 'active'
            for parcel in contract.land_parcel_ids:
                parcel.write({
                    'lease_contract_id': contract.id,
                    'original_owner_id': contract.farmer_id.id
                })
            contract.message_post(body=_("Lease Contract Activated. %s parcels locked under lease.") % len(contract.land_parcel_ids))
            
    def action_consolidate_parcels(self, mega_field_name):
        """
        Consolidates the leased micro-plots into a single manageable Mega-Field,
        while preserving the original ownership DNA in the underlying plots.
        """
        self.ensure_one()
        mega_field = self.env['farm.location'].create({
            'name': mega_field_name,
            'is_land_parcel': True,
            'location_type': 'field'
        })
        
        for parcel in self.land_parcel_ids:
            parcel.write({
                'is_consolidated': True,
                'mega_field_id': mega_field.id
            })
            
        self.message_post(body=_("Consolidated %s micro-plots into Mega-Field: %s") % (len(self.land_parcel_ids), mega_field.name))
        return mega_field

