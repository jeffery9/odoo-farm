# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json
import logging

_logger = logging.getLogger(__name__)

class GovApiController(http.Controller):
    """
    [US-GOV-02] Government REST API Controller.
    Provides secure endpoints for regulatory data exchange.
    """

    @http.route('/agri/gov/api/v1/interventions', type='json', auth='user', methods=['POST'])
    def get_certified_interventions(self, **kwargs):
        """
        Returns a list of completed interventions for a given time period and farm.
        """
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')
        farm_code = kwargs.get('farm_code')
        
        domain = [('state', '=', 'done')]
        if start_date: domain.append(('date_finished', '>=', start_date))
        if end_date: domain.append(('date_finished', '<=', end_date))
        if farm_code:
            farm = request.env['farm.entity'].sudo().search([('code', '=', farm_code)], limit=1)
            if farm: domain.append(('company_id', '=', farm.company_id.id))

        interventions = request.env['mrp.production'].sudo().search(domain)
        
        data = []
        for inv in interventions:
            data.append({
                'id': inv.id,
                'name': inv.name,
                'type': inv.intervention_type,
                'finished_at': inv.date_finished.isoformat(),
                'location': inv.location_id.name,
                'operator': inv.responsible_id.name,
                'snapshot_url': f"/web#id={inv.id}&model=gov.audit.snapshot" # Placeholder
            })
        return {'status': 'success', 'data': data}

    @http.route('/agri/gov/api/v1/snapshot/<string:ref>', type='json', auth='user', methods=['GET'])
    def get_snapshot_by_ref(self, ref):
        """ Returns full signed payload for a specific snapshot """
        snapshot = request.env['gov.audit.snapshot'].sudo().search([('snapshot_ref', '=', ref)], limit=1)
        if not snapshot:
            return {'error': 'Snapshot not found', 'status': 'error'}
            
        return {
            'status': 'success',
            'ref': snapshot.snapshot_ref,
            'data': json.loads(snapshot.snapshot_data),
            'signature': snapshot.digital_signature,
            'verified': snapshot.gov_review_status == 'verified'
        }
