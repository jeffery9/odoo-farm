# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import hashlib
import json
import logging

_logger = logging.getLogger(__name__)

class GovAuditSnapshot(models.Model):
    """
    [US-GOV-01] Immutable Audit Snapshot.
    Stores a read-only, signed copy of farm activities for government inspection.
    """
    _name = 'gov.audit.snapshot'
    _description = 'Government Audit Snapshot'
    _order = 'create_date desc'
    _rec_name = 'snapshot_ref'

    snapshot_ref = fields.Char('Snapshot Reference', required=True, readonly=True)
    source_model = fields.Char('Source Model', required=True, readonly=True)
    source_id = fields.Integer('Source ID', required=True, readonly=True)
    
    # Payload Data
    snapshot_data = fields.Text('Snapshot Payload (JSON)', readonly=True)
    digital_signature = fields.Char('Digital Signature (Hash)', readonly=True)
    
    # Context
    farm_id = fields.Many2one('farm.entity', string='Farm/Entity', readonly=True)
    location_id = fields.Many2one('farm.location', string='Location', readonly=True)
    operator_name = fields.Char('Operator', readonly=True)
    
    # Audit Status
    gov_review_status = fields.Selection([
        ('pending', 'Awaiting Review'),
        ('verified', 'Verified by Gov'),
        ('flagged', 'Flagged for Inspection'),
        ('rejected', 'Audit Rejected')
    ], string='Gov Review Status', default='pending', tracking=True)
    
    gov_auditor_id = fields.Many2one('res.partner', string='Government Auditor', domain=[('is_company', '=', False)])
    gov_comments = fields.Text('Auditor Comments')

    def action_verify_signature(self):
        """ Re-calculates hash to verify data integrity """
        self.ensure_one()
        current_hash = hashlib.sha256(self.snapshot_data.encode()).hexdigest()
        if current_hash == self.digital_signature:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Integrity Verified'),
                    'message': _('The audit snapshot is intact and has not been tampered with.'),
                    'type': 'success',
                    'sticky': False,
                }
            }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Tampering Detected!'),
                    'message': _('CRITICAL: Digital signature mismatch. Data integrity compromised.'),
                    'type': 'danger',
                    'sticky': True,
                }
            }

class AgriInterventionBase(models.AbstractModel):
    _inherit = 'agri.intervention.base'

    @api.model
    def _get_intervention_plugins(self):
        res = super(AgriInterventionBase, self)._get_intervention_plugins()
        res.append({'name': 'gov_audit', 'class': 'agri.intervention.plugin.regulator'})
        return res

class AgriInterventionPluginRegulator(models.AbstractModel):
    """
    [Plugin] Government Oversight.
    Triggers immutable snapshot creation upon intervention completion.
    """
    _name = 'agri.intervention.plugin.regulator'
    _inherit = 'agri.intervention.plugin'

    @api.model
    def execute_hook(self, intervention, hook_point):
        if hook_point == 'post_done':
            self._generate_audit_snapshot(intervention)

    def _generate_audit_snapshot(self, intervention):
        """ Creates a signed record of the completed intervention """
        # 1. Prepare Data
        payload = {
            'name': intervention.name,
            'type': getattr(intervention, 'intervention_type', 'unknown'),
            'date': fields.Datetime.now().isoformat(),
            'location': intervention.location_id.name,
            'inputs': [],
            'evidence_count': len(getattr(intervention, 'evidence_ids', []))
        }
        
        if hasattr(intervention, 'move_raw_ids'):
            for move in intervention.move_raw_ids:
                payload['inputs'].append({
                    'product': move.product_id.name,
                    'qty': move.product_uom_qty,
                    'reg_no': getattr(move.product_id, 'reg_cert_no', 'N/A')
                })

        json_data = json.dumps(payload, sort_keys=True)
        
        # 2. Digital Signature (Simple SHA256 for now)
        signature = hashlib.sha256(json_data.encode()).hexdigest()
        
        # 3. Create Snapshot
        self.env['gov.audit.snapshot'].sudo().create({
            'snapshot_ref': f"GOV-{intervention.name}",
            'source_model': intervention._name,
            'source_id': intervention.id,
            'snapshot_data': json_data,
            'digital_signature': signature,
            'farm_id': self.env['farm.entity'].search([('company_id', '=', intervention.company_id.id)], limit=1).id,
            'location_id': intervention.location_id.id,
            'operator_name': intervention.responsible_id.name
        })
        _logger.info(f"Government Audit Snapshot created for {intervention.name}")
