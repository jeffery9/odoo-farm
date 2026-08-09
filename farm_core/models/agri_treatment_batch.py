# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class AgriTreatmentBatch(models.Model):
    _name = 'agri.treatment.batch'
    _description = 'Agricultural Treatment Batch / Processing Campaign Run (农耕与生物处理批次/炉次)'
    _order = 'id desc'

    name = fields.Char(
        string='Batch Code',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New')
    )
    carrier_ids = fields.One2many(
        'stock.matter.tracking',
        'treatment_batch_id',
        string='Active Material Carriers (物料载体)'
    )
    treatment_temperature = fields.Float(
        string='Target Treatment Temp (°C)',
        default=25.0
    )
    state = fields.Selection([
        ('draft', 'Draft / 计划中'),
        ('processing', 'Processing / 加工处理中'),
        ('done', 'Done / 完成'),
        ('cancel', 'Cancelled / 取消')
    ], string='Batch State', default='draft', required=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name') or vals.get('name') == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('agri.treatment.batch') or '/'
        return super(AgriTreatmentBatch, self).create(vals_list)

    def action_start(self):
        self.ensure_one()
        if not self.carrier_ids:
            raise UserError(_("Cannot start treatment run with empty carriers."))
        
        # Enforce Carrier Admission Rules based on physical graph check (工序准入校验)
        for carrier in self.carrier_ids:
            # 1. State validation
            if carrier.carrier_state not in ['idle', 'loading']:
                raise ValidationError(_(
                    "Carrier Admission Rule Violation: Carrier %s is in state [%s]. "
                    "Only carriers in 'idle' or 'loading' state can enter the workstation."
                ) % (carrier.name, carrier.carrier_state))
            # 2. GxP / pedigree validation
            if carrier.dna_integrity_score < 50.0:
                raise ValidationError(_(
                    "Carrier Admission Rule Violation: Carrier %s has DNA purity %s%%, "
                    "which fails the high-fidelity quality safety limit (minimum 50%%)."
                ) % (carrier.name, carrier.dna_integrity_score))
        
        # Walk the graph and transition linked carriers to processing
        for carrier in self.carrier_ids:
            carrier.write({'carrier_state': 'processing'})
            
        self.write({'state': 'processing'})
        return True

    def action_complete(self):
        self.ensure_one()
        if self.state != 'processing':
            raise UserError(_("Only processing batches can be completed."))
            
        # Transition linked carriers to QC
        for carrier in self.carrier_ids:
            carrier.write({'carrier_state': 'qc'})
            
        self.write({'state': 'done'})
        return True
