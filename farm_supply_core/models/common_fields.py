from odoo import models, fields, api


class SupplyCommonFieldsMixin(models.AbstractModel):
    """
    Common fields for supply chain models
    """
    _name = 'supply.common.fields.mixin'
    _description = 'Supply Chain Common Fields Mixin'

    # Tracking and compliance fields
    is_compliance_approved = fields.Boolean("Compliance Approved", default=True)
    compliance_date = fields.Date("Compliance Date")
    safety_check_required = fields.Boolean("Safety Check Required", default=False)

    # Quality and specification fields
    quality_grade = fields.Selection([
        ('grade_a', 'Grade A (Premium)'),
        ('grade_b', 'Grade B (Standard)'),
        ('grade_c', 'Grade C (Economy)'),
        ('grade_d', 'Grade D (Below Standard)'),
    ], string='Quality Grade')

    quality_score = fields.Float('Quality Score', help="Quality score out of 100")

    # Shelf life and expiration
    shelf_life_days = fields.Integer("Shelf Life (Days)")
    expiration_date = fields.Date("Expiration Date")
    best_before_date = fields.Date("Best Before Date")

    # Traceability
    batch_number = fields.Char("Batch Number")
    production_date = fields.Date("Production Date")
    supplier_lot_number = fields.Char("Supplier Lot Number")