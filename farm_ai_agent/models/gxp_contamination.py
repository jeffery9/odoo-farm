# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AgriGxpContaminationIncident(models.Model):
    _name = 'agri.gxp.contamination.incident'
    _description = 'GxP Contamination Incident'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Incident Reference", required=True, copy=False, readonly=True, default=lambda self: _('New'))
    source_carrier_id = fields.Many2one('stock.matter.tracking', string="Source Matter Carrier", required=True)
    contamination_type = fields.Selection([
        ('chemical', 'Chemical (化学污染)'),
        ('biological', 'Biological (生物疫病)'),
        ('heavy_metal', 'Heavy Metal (重金属超标)')
    ], string="Contamination Type", required=True, default='chemical')
    description = fields.Text("Detailed Description")
    incident_date = fields.Date("Incident Date", default=fields.Date.context_today, required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('quarantined', 'Quarantined'),
        ('closed', 'Closed')
    ], string="State", default='draft', required=True, tracking=True)
    affected_carrier_ids = fields.Many2many('stock.matter.tracking', 'agri_gxp_contam_incident_tracking_rel', 'incident_id', 'tracking_id', string="Affected Downstream Carriers", readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('agri.gxp.contamination.incident') or '/'
        return super(AgriGxpContaminationIncident, self).create(vals_list)

    def action_quarantine_downstream(self):
        """
        Runs DFS recursively to identify all downstream stock.matter.tracking carriers linked via 
        stock.matter.tracking.link and marks them quarantined.
        """
        for incident in self:
            if not incident.source_carrier_id:
                continue
            
            visited_ids = set()
            to_quarantine_ids = set()

            def dfs(carrier_id):
                if carrier_id in visited_ids:
                    return
                visited_ids.add(carrier_id)
                
                links = self.env['stock.matter.tracking.link'].search([('parent_id', '=', carrier_id)])
                for link in links:
                    child_id = link.child_id.id
                    to_quarantine_ids.add(child_id)
                    dfs(child_id)

            # Start DFS trace
            dfs(incident.source_carrier_id.id)

            if to_quarantine_ids:
                affected_carriers = self.env['stock.matter.tracking'].browse(to_quarantine_ids)
                affected_carriers.with_context(bypass_carrier_transition_rules=True).write({'carrier_state': 'quarantine'})
                
                incident.write({
                    'affected_carrier_ids': [(6, 0, affected_carriers.ids)],
                    'state': 'quarantined'
                })

                for carrier in affected_carriers:
                    body = f"""<div style="border: 2px solid #ef4444; padding: 12px; background-color: #fef2f2; border-radius: 4px; font-family: monospace;">
                        <h4 style="color: #ef4444; margin: 0 0 8px 0; font-size: 14px;">⚠️ GXP PREEMPTIVE QUARANTINE (GxP 预警隔离)</h4>
                        <p style="margin: 4px 0; font-size: 12px;">This carrier has been quarantined due to upstream contamination incident: <strong>{incident.name}</strong></p>
                        <p style="margin: 4px 0; font-size: 11px; color: #7f1d1d;"><strong>Source Contaminant:</strong> {incident.source_carrier_id.display_name}</p>
                    </div>"""
                    carrier.message_post(body=body)
            else:
                incident.write({'state': 'quarantined'})
        return True


class StockMatterTracking(models.Model):
    _inherit = 'stock.matter.tracking'

    carrier_state = fields.Selection(
        selection_add=[('quarantine', 'Quarantine / 隔离中')],
        ondelete={'quarantine': 'cascade'}
    )


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('location_id') and vals.get('package_id'):
                new_loc = self.env['stock.location'].browse(vals['location_id'])
                if not new_loc.is_quarantine_location:
                    tracking = self.env['stock.matter.tracking'].search([('package_id', '=', vals['package_id'])], limit=1)
                    if tracking and tracking.carrier_state == 'quarantine':
                        raise ValidationError(_(
                            "GXP_QUARANTINE_LOCKDOWN: Quarantined carrier can only be moved to a designated quarantine location. "
                            "(隔离区管控锁定：处于隔离状态的载体仅允许移动到指定的隔离区库位。)"
                        ))
        return super().create(vals_list)

    def write(self, vals):
        if 'location_id' in vals:
            new_loc_id = vals.get('location_id')
            if new_loc_id:
                new_loc = self.env['stock.location'].browse(new_loc_id)
                if not new_loc.is_quarantine_location:
                    for quant in self:
                        if quant.package_id:
                            tracking = self.env['stock.matter.tracking'].search([('package_id', '=', quant.package_id.id)], limit=1)
                            if tracking and tracking.carrier_state == 'quarantine':
                                raise ValidationError(_(
                                    "GXP_QUARANTINE_LOCKDOWN: Quarantined carrier can only be moved to a designated quarantine location. "
                                    "(隔离区管控锁定：处于隔离状态的载体仅允许移动到指定的隔离区库位。)"
                                ))
        return super().write(vals)


class StockLocation(models.Model):
    _inherit = 'stock.location'

    is_quarantine_location = fields.Boolean("Is Quarantine Location (GxP 防疫隔离区库位)", default=False)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        for picking in self:
            if picking.location_dest_id.usage in ['customer', 'supplier']:
                packages = picking.move_line_ids.mapped('package_id') | picking.move_line_ids.mapped('result_package_id')
                carriers = self.env['stock.matter.tracking'].search([
                    ('package_id', 'in', packages.ids)
                ])
                if any(c.carrier_state == 'quarantine' for c in carriers):
                    raise ValidationError(_(
                        "GXP_OUTBOUND_BLOCKED: Cannot validate delivery. Package containing quarantined material is detected in shipment! "
                        "(GxP 发运阻断：检测到本拣货单包含处于隔离状态的物料，禁止执行出库发货！)"
                    ))
        return super(StockPicking, self).button_validate()
