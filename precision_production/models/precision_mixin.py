# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import json

class PrecisionProductionMixin(models.AbstractModel):
    """
    [US-200-XP] Performance & Process Control DNA.
    Enhanced to support SPC-like monitoring and personnel accountability.
    """
    _name = 'precision.production.mixin'
    _description = 'Precision Production Active DNA'

    # 1. Performance KPIs
    yield_confidence = fields.Float("Yield Confidence (%)", default=100.0)
    efficiency_index = fields.Float("Efficiency Index", default=1.0, help="1.0 = On track, <1.0 = Delayed")
    quality_score = fields.Float("Quality Score", default=100.0, help="Based on grading results")
    
    # 2. Process Control (SPC Concepts)
    process_status = fields.Selection([
        ('stable', 'Stable'),
        ('drifting', 'Drifting'),
        ('out_of_control', 'Out of Control')
    ], string="Process Stability", default='stable', tracking=True)
    
    is_process_locked = fields.Boolean("Execution Hold", default=False, tracking=True)
    lock_reason = fields.Char("Hold Reason")

    # [LOSSLESS] Original Sensing & State
    last_telemetry_data = fields.Text("Latest Telemetry (JSON)")
    last_calibration_date = fields.Datetime("Last Calibration")
    active_instruction_json = fields.Text("Active Skill Command")
    skill_execution_status = fields.Selection([
        ('idle', 'Idle'), ('triggered', 'Skill Triggered'),
        ('executing', 'In Progress'), ('success', 'Applied'), ('failed', 'Failed')
    ], string="Active Skill Status", default='idle')

    # [LOSSLESS] Multi-Grade Output & Interventions
    graded_output_ids = fields.One2many('precision.graded.output', 'res_id', 
                                       domain=lambda self: [('res_model', '=', self._name)])
    intervention_ids = fields.One2many('precision.intervention.log', 'res_id', 
                                      domain=lambda self: [('res_model', '=', self._name)])

    def action_hold_execution(self, reason):
        self.ensure_one()
        self.write({'is_process_locked': True, 'lock_reason': reason})
        self.action_log_intervention(_("PROCESS HOLD: %s") % reason, intervention_type='active')

    def action_release_hold(self):
        self.ensure_one()
        self.write({'is_process_locked': False, 'lock_reason': False})
        self.action_log_intervention(_("PROCESS RELEASED"), intervention_type='manual')

    # [LOSSLESS] Existing methods
    def apply_corrective_skill(self, skill_payload, basis_id=False):
        self.ensure_one()
        self.active_instruction_json = json.dumps(skill_payload, indent=2)
        self.skill_execution_status = 'triggered'
        self.action_log_intervention(
            _("ACTIVE SKILL: %s") % skill_payload.get('action', 'Unknown'),
            intervention_type='active', basis_id=basis_id
        )
        return True

    def action_log_intervention(self, name, intervention_type='manual', basis_id=False):
        self.ensure_one()
        return self.env['precision.intervention.log'].create({
            'res_model': self._name, 'res_id': self.id,
            'name': name, 'intervention_type': intervention_type,
            'basis_id': basis_id, 'user_id': self.env.user.id
        })

    def action_generate_graded_lots(self):
        """ [Product Logic] Uses Odoo Native By-products for Grading. """
        self.ensure_one()
        total_score = 0
        total_qty = 0
        for line in self.graded_output_ids:
            move = self.move_finished_ids.filtered(lambda m: m.product_id == line.product_id and m.state not in ['done', 'cancel'])[:1]
            if not move:
                move = self.env['stock.move'].create({
                    'name': self.name, 'product_id': line.product_id.id,
                    'product_uom_qty': line.quantity, 'product_uom': line.product_id.uom_id.id,
                    'production_id': self.id, 'location_id': self.product_id.property_stock_production.id,
                    'location_dest_id': self.location_dest_id.id,
                })
            else:
                move.write({'product_uom_qty': line.quantity})
            
            # KPI: Quality Scoring (Premium=100, Standard=80, Fail=0)
            weight = {'premium': 100, 'standard': 80, 'fail': 0}
            total_score += line.quantity * weight.get(line.grade, 0)
            total_qty += line.quantity

            lot = self.env['stock.lot'].create({
                'name': f"{self.name}-{line.grade.upper()}-{fields.Date.today()}",
                'product_id': line.product_id.id, 'quality_grade': line.grade
            })
            move.move_line_ids.unlink()
            self.env['stock.move.line'].create({
                'move_id': move.id, 'product_id': line.product_id.id, 'lot_id': lot.id,
                'quantity': line.quantity, 'product_uom_id': line.product_id.uom_id.id,
                'location_id': move.location_id.id, 'location_dest_id': move.location_dest_id.id,
            })
        
        if total_qty:
            self.quality_score = total_score / total_qty
        return True
