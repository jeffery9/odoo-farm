from odoo import models, fields, api

class AgriEvidenceMixin(models.AbstractModel):
    """
    [Level 2: Physical Proof] - Fundamental evidence and audit trail for agricultural activities.
    This mixin ensures every biological or physical intervention has an evidence chain.
    """
    _name = 'agri.evidence.mixin'
    _description = 'Agri Evidence & Audit Mixin'

    evidence_ids = fields.Many2many('ir.attachment', string="Physical Evidence", help="Photos, IoT sensor logs, or PDF certificates.")
    evidence_hash = fields.Char("Evidence Hash", readonly=True, help="Cryptographic hash of the evidence for tamper-proof auditing.")
    evidence_source = fields.Selection([
        ('manual', 'Manual Entry'),
        ('iot', 'IoT Device'),
        ('vision', 'AI Vision Agent'),
        ('satellite', 'Remote Sensing')
    ], string="Evidence Source", default='manual')
    
    is_verified = fields.Boolean("Evidence Verified", default=False)
    verified_by_id = fields.Many2one('res.users', string="Verified By")
    verification_at = fields.Datetime("Verification Timestamp")

    @api.model
    def _generate_evidence_hash(self):
        """Standardized method to generate evidence hash (stub for future implementation)"""
        return False
