from odoo import models, fields, api, _
import json
import logging
import uuid

_logger = logging.getLogger(__name__)

class A2AProtocol(models.AbstractModel):
    _name = 'agri.a2a.protocol'
    _description = 'Agricultural Agent-to-Agent Protocol'

    def construct_plan_payload(self, agent_id, intent_type, business_object):
        self.ensure_one()
        spatial_context = business_object.get_spatial_context() if hasattr(business_object, 'get_spatial_context') else {}
        fingerprint = business_object.quality_fingerprint if hasattr(business_object, 'quality_fingerprint') else ""
        
        payload = {
            'header': {
                'message_id': str(uuid.uuid4()),
                'sender_agent': agent_id,
                'timestamp': fields.Datetime.now().isoformat(),
                'protocol_version': '2026.1'
            },
            'intent': {
                'type': intent_type,
                'target_id': f"{business_object._name}:{business_object.id}"
            },
            'context_memory': {
                'spatial_grid': spatial_context.get('grid_id'),
                'esg_score': getattr(business_object, 'esg_score', 100),
                'carbon_intensity': getattr(business_object, 'carbon_intensity', 0.0)
            },
            'evidence_bundle': {
                'quality_fingerprint': json.loads(fingerprint) if fingerprint else {},
                'audit_confidence': getattr(business_object, 'audit_confidence', 0.0)
            }
        }
        return payload

    def parse_and_validate_plan(self, payload_json):
        try:
            payload = json.loads(payload_json)
            if 'header' not in payload or 'intent' not in payload:
                return {'status': 'error', 'reason': 'Invalid PlanAPI structure'}
            
            # Post to Chatter of the related object
            target_info = payload['intent']['target_id'].split(':')
            if len(target_info) == 2:
                model, res_id = target_info
                res_id = int(res_id)
                record = self.env[model].browse(res_id)
                if record.exists() and hasattr(record, 'message_post'):
                    body = _(
                        "<b>Agent A2A Notification</b><br/>"
                        "<b>Intent:</b> %s<br/>"
                        "<b>Sender:</b> %s<br/>"
                        "<b>Spatial Proof:</b> %s<br/>"
                        "<b>Audit Confidence:</b> %s%%"
                    ) % (
                        payload['intent']['type'],
                        payload['header']['sender_agent'],
                        payload['context_memory'].get('spatial_grid', 'N/A'),
                        round(payload['evidence_bundle'].get('audit_confidence', 0) * 100, 2)
                    )
                    record.message_post(body=body, message_type='notification', subtype_xmlid='mail.mt_note')
            
            return {'status': 'accepted', 'message_id': payload['header']['message_id']}
        except Exception as e:
            return {'status': 'error', 'reason': str(e)}

class A2AMessage(models.Model):
    _name = 'agri.a2a.message'
    _description = 'Agricultural Agent Communication Log'
    _inherit = ['agri.a2a.protocol']

    name = fields.Char("Message ID", required=True)
    sender_id = fields.Char("Sender Agent")
    receiver_id = fields.Char("Receiver Agent")
    payload = fields.Text("PlanAPI Payload")
    state = fields.Selection([
        ('sent', 'Sent'),
        ('received', 'Received'),
        ('processed', 'Processed'),
        ('disputed', 'Disputed')
    ], default='sent')
    
    related_object = fields.Reference(
        selection=[('mrp.production', 'Intervention'), ('stock.lot', 'Lot')],
        string="Related Object"
    )

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            if record.payload:
                record.parse_and_validate_plan(record.payload)
        return records