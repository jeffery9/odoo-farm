from odoo import models, fields, api
from odoo.tools.float_utils import float_compare, float_is_zero
import logging

_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    """
    US-09-20: FEFO (First Expired First Out) picking strategy implementation
    """
    _inherit = 'stock.move'

    def _get_available_quantity(self, product_id, location_id, lot_id=None, package_id=None, owner_id=None, strict=False):
        """
        Override to consider FEFO when checking available quantities
        """
        quant_domain = self._get_available_quantity_domain(product_id, location_id, lot_id, package_id, owner_id, strict)
        quants = self.env['stock.quant'].with_context(lang=False).search(quant_domain)

        # If the product has lot/serial tracking, apply FEFO prioritization
        if product_id.tracking in ['lot', 'serial']:
            # Sort quants by expiration date (earliest first for FEFO)
            quants = quants.sorted(key=lambda q: q.lot_id.expiration_date or fields.Date.max)

        available_qty = sum(quants.mapped('quantity')) - sum(quants.mapped('reserved_quantity'))
        return available_qty

    def _update_reserved_quantity(self, need, available_quantity, location_id, lot_ids=None, package_id=None, owner_id=None, strict=True):
        """
        Override to reserve quantities according to FEFO (First Expired First Out) logic
        """
        if not lot_ids and self.product_id.tracking == 'none':
            return super()._update_reserved_quantity(
                need, available_quantity, location_id, lot_ids=lot_ids, package_id=package_id,
                owner_id=owner_id, strict=strict)

        # Create the necessary reservations
        if self.product_id.tracking != 'none':
            rounding = self.product_id.uom_id.rounding
            available_quants = self.env['stock.quant']

            # Get all available quants for this product at the location
            quant_domain = [
                ('product_id', '=', self.product_id.id),
                ('location_id', 'child_of', location_id.id) if not strict else [('location_id', '=', location_id.id)],
                ('quantity', '>', 0),
                ('reserved_quantity', '<', 'quantity'),
            ]

            # Add lot filter if specified
            if lot_ids:
                quant_domain.append(('lot_id', 'in', lot_ids.ids))

            available_quants = self.env['stock.quant'].search(quant_domain)

            # Apply FEFO: Sort by expiration date (earliest first)
            if self.product_id.tracking in ['lot', 'serial']:
                available_quants = available_quants.sorted(
                    key=lambda q: (q.lot_id.expiration_date or fields.Date.max, q.create_date)
                )

            # Reserve quantities following FEFO logic
            for quant in available_quants:
                if float_is_zero(need, precision_rounding=rounding):
                    break

                max_reservation = min(need, quant.quantity - quant.reserved_quantity)
                if float_is_zero(max_reservation, precision_rounding=rounding):
                    continue

                self.env['stock.quant'].quants_reserve([(quant, max_reservation)], self)
                need -= max_reservation

            return need
        else:
            # For products without tracking, use default behavior
            return super()._update_reserved_quantity(
                need, available_quantity, location_id, lot_ids=lot_ids, package_id=package_id,
                owner_id=owner_id, strict=strict)

    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        """
        Override to ensure FEFO is considered when creating move lines
        """
        vals = super()._prepare_move_line_vals(quantity=quantity, reserved_quant=reserved_quant)

        # If we have a reserved quant with a lot and the product has expiration tracking
        if reserved_quant and reserved_quant.lot_id and self.product_id.tracking in ['lot', 'serial']:
            vals['lot_id'] = reserved_quant.lot_id.id
            vals['expiration_date'] = reserved_quant.lot_id.expiration_date  # Use for display in move line

        return vals


class StockQuant(models.Model):
    """
    Extension to support FEFO prioritization during stock allocation
    """
    _inherit = 'stock.quant'

    @api.model
    def _get_removal_strategy(self, location_id, product_id):
        """
        Define removal strategy for FEFO
        """
        # If product has lot tracking and expiration dates, use FEFO
        if product_id.tracking in ['lot', 'serial'] and product_id.use_expiration_date:
            return 'fefo'
        else:
            # Default to FIFO for other cases
            return super()._get_removal_strategy(location_id, product_id)

    def _get_removal_candidates(self, move):
        """
        Get quants eligible for removal based on FEFO strategy
        """
        removal_strategy = self._get_removal_strategy(move.location_id, move.product_id)

        if removal_strategy == 'fefo':
            # Get quants sorted by expiration date (earliest first)
            quants = self._gather(move.product_id, move.location_id, lot_ids=move.lot_ids, package_ids=move.package_id,
                                 owner_ids=move.picking_id.owner_id, strict=True)

            # Filter out expired lots for FEFO
            today = fields.Date.today()
            valid_quants = quants.filtered(lambda q: not q.lot_id.expiration_date or q.lot_id.expiration_date >= today)

            # Sort by expiration date (earliest first), then by create_date as tie-breaker
            valid_quants = valid_quants.sorted(
                key=lambda q: (q.lot_id.expiration_date or fields.Date.max, q.create_date)
            )

            return valid_quants
        else:
            # For non-FEFO cases, use standard method
            return super()._get_removal_candidates(move)


class StockPicking(models.Model):
    """
    Extended to support FEFO operations
    """
    _inherit = 'stock.picking'

    def _check_FEFO_compliance(self):
        """
        Check FEFO compliance for all moves in this picking
        """
        for move in self.move_ids_without_package:
            for move_line in move.move_line_ids:
                if move_line.lot_id and move_line.product_id.tracking in ['lot', 'serial']:
                    # Use the existing method to check compliance
                    self.check_fefo_compliance_for_move_line(move_line)

    def button_validate(self):
        """
        Override to check FEFO compliance before validating picking
        """
        # Check FEFO compliance before validation
        for move in self.move_ids_without_package:
            for move_line in move.move_line_ids:
                if move_line.lot_id and move_line.product_id.tracking in ['lot', 'serial']:
                    self.check_fefo_compliance_for_move_line(move_line)

        return super().button_validate()


class ProductTemplate(models.Model):
    """
    Add FEFO configuration to products
    """
    _inherit = 'product.template'

    # FEFO-related field to indicate if this product should follow FEFO strategy
    use_fefo_strategy = fields.Boolean(
        'Use FEFO Strategy',
        help='Apply First Expired First Out strategy for this product',
        default=False
    )


class ProductProduct(models.Model):
    """
    Add FEFO configuration to specific products
    """
    _inherit = 'product.product'

    # Inherit the FEFO strategy from the template
    use_fefo_strategy = fields.Boolean(
        'Use FEFO Strategy',
        related='product_tmpl_id.use_fefo_strategy',
        store=True,
        readonly=True
    )