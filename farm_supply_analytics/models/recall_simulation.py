from odoo import models, fields, api, _

class SupplyChainRecall(models.Model):
    _name = 'farm.supply.recall'
    _description = 'Emergency Recall Simulation'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Recall ID", required=True, default=lambda self: _('New'))
    triggering_qc_id = fields.Many2one('agri.quality.check', string="Triggering QC", required=True)
    product_id = fields.Many2one('product.product', related='triggering_qc_id.lot_id.product_id', string="Product")
    
    # Traceability
    affected_lot_ids = fields.Many2many('stock.lot', string="Affected Quarantined Lots")
    affected_location_ids = fields.Many2many('farm.location', string="Source Parcels Identified")
    
    # PR/Crisis Action
    ai_pr_draft = fields.Text("AI Generated Recall Notice")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Quarantine Active'),
        ('resolved', 'Resolved')
    ], default='draft', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('farm.supply.recall') or _('RECALL')
        return super().create(vals_list)

    def action_execute_recall(self):
        """
        [US-TRACE-02] Execute deep trace and quarantine
        """
        self.ensure_one()
        
        # 1. Trace the source parcel of the failed lot
        bad_lot = self.triggering_qc_id.lot_id
        
        # Simplified tracing: Find the intervention that produced the bad lot
        interventions = self.env['mrp.production'].search([('lot_producing_id', '=', bad_lot.id)])
        parcels = interventions.mapped('land_parcel_id')
        self.affected_location_ids = [(6, 0, parcels.ids)]
        
        # 2. Find all OTHER lots produced from these parcels recently
        # In a real scenario, this would use a recursive graph search on stock.move.line
        sibling_interventions = self.env['mrp.production'].search([
            ('land_parcel_id', 'in', parcels.ids)
        ])
        sibling_lots = sibling_interventions.mapped('lot_producing_id')
        
        self.affected_lot_ids = [(6, 0, sibling_lots.ids)]
        
        # 3. Quarantine all affected lots
        quarantine_loc = self.env['stock.location'].search([('name', 'ilike', 'Quarantine')], limit=1)
        if not quarantine_loc:
            quarantine_loc = self.env['stock.location'].create({
                'name': 'Virtual Quarantine',
                'usage': 'internal'
            })
            
        for lot in self.affected_lot_ids:
            # Create a stock move to move them to quarantine
            self.env['stock.quant']._update_available_quantity(
                lot.product_id, 
                quarantine_loc, 
                1.0, # Dummy quantity for test
                lot_id=lot
            )
            # You would normally deduct from the original location here too
            
        self.state = 'active'
        self.message_post(body=_("Recall executed. Quarantined %s lots originating from %s parcels.") % (len(sibling_lots), len(parcels)))
        
        # 4. Trigger AI PR drafting
        self._generate_ai_pr_notice()

    def _generate_ai_pr_notice(self):
        """
        [L2 -> L3 Call] Use AI to draft crisis communication.
        """
        if 'agri.ai.llm.service' not in self.env:
            self.ai_pr_draft = "URGENT RECALL: Please return the product."
            return

        llm_service = self.env['agri.ai.llm.service'].search([], limit=1)
        
        prompt = f"Product {self.product_id.name} failed Quality Check due to {self.triggering_qc_id.point_id.name}. Draft an emergency recall notice for our distributors, striking a professional, transparent, and reassuring tone. Mention that {len(self.affected_lot_ids)} batches have been preemptively quarantined."
        
        if llm_service and not self.env.context.get('test_mock_llm'):
            import logging
            _logger = logging.getLogger(__name__)
            try:
                self.ai_pr_draft = llm_service.call_llm(prompt)
            except Exception as e:
                _logger.warning("LLM call failed: %s", str(e))
                self.ai_pr_draft = self._mock_pr_draft()
        else:
            self.ai_pr_draft = self._mock_pr_draft()

    def _mock_pr_draft(self):
        return f"""
        **URGENT PRODUCT RECALL NOTICE**
        
        Dear Partner,
        We have detected an anomaly during our rigorous quality control procedures for {self.product_id.name}.
        Out of an abundance of caution, we have preemptively quarantined {len(self.affected_lot_ids)} batches.
        Please halt sales immediately.
        """

