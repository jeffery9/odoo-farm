from odoo import models, fields

class CooperativeMemberExtensionEquipment(models.Model):    _inherit = 'cooperative.member'

    machinery_rental_ids = fields.One2many('machinery.rental', 'renter_member_id', string='Machinery Rentals')

class CooperativeEntityExtensionEquipment(models.Model):    _inherit = 'cooperative.entity'

    shared_machinery_ids = fields.One2many('shared.machinery.pool', 'cooperative_id', string='Shared Machinery')
