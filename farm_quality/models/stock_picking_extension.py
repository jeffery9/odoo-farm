from odoo import models, fields, api, _
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        # Only check outgoing shipments
        for picking in self.filtered(lambda p: p.picking_type_id.code == 'outgoing'):
            for move_line in picking.move_line_ids:
                if move_line.lot_id:
                    self._check_lot_chemical_safety(move_line.lot_id)
        
        return super().button_validate()

    def _check_lot_chemical_safety(self, lot):
        """
        [US-TRACE-01] Deep Traceability Safety Check
        Traces back to the mrp.production (Intervention) that produced this lot,
        and scans all consumed materials for forbidden chemicals.
        """
        # Find interventions that produced this lot
        if 'mrp.production' not in self.env or 'lot_producing_id' not in self.env['mrp.production']._fields:
            return
        interventions = self.env['mrp.production'].search([('lot_producing_id', '=', lot.id)])
        for intervention in interventions:
            for move in intervention.move_raw_ids:
                product = move.product_id
                if product.is_agricultural_chemical and product.is_forbidden:
                    # Trigger an automatic Quality Alert
                    self._trigger_quality_alert(lot, intervention, product)
                    raise UserError(_(
                        "Safety Violation: Lot '%s' is tainted!\\n"
                        "Intervention '%s' consumed forbidden chemical: '%s'."
                    ) % (lot.name, intervention.name, product.name))
                    
    def _trigger_quality_alert(self, lot, intervention, chemical):
        alert_val = {
            'name': _('Tainted Lot Alert: %s') % lot.name,
            'lot_id': lot.id,
            'reason': _('Forbidden chemical used during production: %s') % chemical.name,
            'priority': '1', # High priority
        }
        if 'quality.alert' in self.env:
            self.env['quality.alert'].create(alert_val)

