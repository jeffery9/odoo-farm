from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import math
import base64
import datetime
import re


class AgriInterventionMixin(models.AbstractModel):
    """
    Abstract base model for agricultural intervention functionality.
    This mixin provides shared logic across different agricultural intervention implementations.
    """
    _name = 'agri.intervention.mixin'
    _description = 'Agri Agricultural Intervention Shared Logic'
    _inherit = ['agri.intervention.base', 'agri.resource.consumption.mixin', 'agri.incident.alert.mixin']

    # Registry for intervention plugins
    @api.model
    def _get_intervention_plugins(self):
        res = super(AgriInterventionMixin, self)._get_intervention_plugins()
        res.extend([
            {'name': 'weather_gating', 'class': 'agri.intervention.plugin.weather'},
            {'name': 'spatial_audit', 'class': 'agri.intervention.plugin.spatial'},
            {'name': 'yield_calibration', 'class': 'agri.intervention.plugin.yield'},
            {'name': 'nutrient_tracking', 'class': 'agri.intervention.plugin.nutrient'},
            {'name': 'compliance', 'class': 'agri.intervention.plugin.compliance'},
            {'name': 'labor_tracking', 'class': 'agri.intervention.plugin.labor'},
            {'name': 'iot_monitoring', 'class': 'agri.intervention.plugin.iot'},
        ])
        return res

    # Basic intervention fields (location_id is now in base)
    agri_task_id = fields.Many2one(
        'project.task',
        string="Production Task",
        help="The specific production task this intervention belongs to."
    )

    campaign_id = fields.Many2one(
        'farm.agricultural.campaign',
        string="Campaign/Season",
        help="The production season this intervention belongs to."
    )

    # ---------------------------------------------------------
    # [Agri-Precision Absorbed DNA] 
    # Yield Calibration, Cycle Counting, and IoT Status
    # ---------------------------------------------------------
    
    # 1. Uncertainty: Dynamic Yield Tracking
    expected_yield_accuracy = fields.Float("Expected Yield Accuracy (%)", default=100.0)
    last_metrology_date = fields.Datetime("Last Calibration/Sampling")

    # 2. Intervention: Cycle Tracking
    intervention_count = fields.Integer("Intervention Cycles", default=0, copy=False)

    # 3. IoT Integration: Environment Condition
    iot_device_ids = fields.Many2many(
        'iiot.device',
        string='IoT Devices',
        help='IoT devices directly associated with this intervention for environmental gating.'
    )
    iot_status = fields.Selection([
        ('normal', 'Normal'),
        ('monitoring', 'Monitoring'),
        ('warning', 'Warning'),
        ('critical', 'Critical')
    ], string="IoT Environmental Status", default='normal', tracking=True)

    def action_update_yield_estimate(self, new_qty):
        """ [Uncertainty] Mid-process yield calibration based on field sampling. """
        self.ensure_one()
        self.product_qty = new_qty
        self.last_metrology_date = fields.Datetime.now()
        self.message_post(body=_("YIELD CALIBRATION: New expected quantity set to %s.") % new_qty)

    def action_trigger_iot_based_intervention(self, sensor_readings_summary):
        """
        Automatically adjust IoT status via Plugin.
        """
        self.ensure_one()
        self.intervention_count += 1
        
        # Use IoT Plugin
        plugin = self.env['agri.intervention.plugin.iot']
        plugin.update_iot_status(self, sensor_readings_summary)
        return True


    # Agricultural-specific intervention classification
    intervention_type = fields.Selection([
        ('tillage', 'Soil Preparation'),
        ('sowing', 'Sowing/Planting'),
        ('fertilizing', 'Fertilizing'),
        ('irrigation', 'Irrigation'),
        ('protection', 'Crop Protection'),
        ('aerial_spraying', 'Aerial Spraying'),
        ('harvesting', 'Harvesting'),
        ('feeding', 'Feeding'),
        ('medical', 'Medical/Prevention'),
    ], string="Intervention Type")

    # Ekylibre Mapping: Intervention Parameters
    # doer_ids = fields.Many2many('hr.employee', string="Doers/Workers")
    tool_ids = fields.Many2many('maintenance.equipment', string="Tools/Machinery")

    procedure_name = fields.Char("Procedure/Method", help="e.g. Mechanical sowing, manual weeding")

    # US-041-02: China Real-name Registration
    operator_id_card = fields.Char("Operator ID Card", help="Required for pesticide/veterinary real-name registration.")
    product_registration_no = fields.Char("Product Registration No.", help="Pesticide or veterinary product registration number.")

    # Harvest Grading [US-002-04]
    grade_a_qty = fields.Float("Grade A Quantity")
    grade_b_qty = fields.Float("Grade B Quantity")
    grade_c_qty = fields.Float("Grade C Quantity")

    @api.constrains('grade_a_qty', 'grade_b_qty', 'grade_c_qty')
    def _check_graded_quantities(self):
        for intervention in self:
            if intervention.intervention_type == 'harvesting' and (intervention.grade_a_qty < 0 or intervention.grade_b_qty < 0 or intervention.grade_c_qty < 0):
                raise UserError(_("Graded quantities cannot be negative."))

    # Ekylibre Mapping: Costing [US-Mapping]
    input_cost = fields.Float("Input Cost", compute='_compute_agri_costs', store=True, precompute=True)
    tool_cost = fields.Float("Tool/Machinery Cost", compute='_compute_agri_costs', store=True, precompute=True)
    doer_cost = fields.Float("Labor Cost", compute='_compute_agri_costs', store=True, precompute=True)
    energy_cost = fields.Float("Energy/Utility Cost", compute='_compute_agri_costs', store=True, precompute=True)
    total_agri_cost = fields.Float("Total Intervention Cost", compute='_compute_agri_costs', store=True, precompute=True)

    # US-002-03: Soil Nutrient Inputs (RESTORED)
    pure_n_qty = fields.Float("Pure Nitrogen (N) kg", compute='_compute_agri_costs', store=True, precompute=True)
    pure_p_qty = fields.Float("Pure Phosphorus (P) kg", compute='_compute_agri_costs', store=True, precompute=True)
    pure_k_qty = fields.Float("Pure Potassium (K) kg", compute='_compute_agri_costs', store=True, precompute=True)

    # @api.depends('move_raw_ids.state', 'move_raw_ids.product_uom_qty', 'workorder_ids.duration', 'is_working')
    def _compute_agri_costs(self):
        for mo in self:
            # 1. 投入品成本 (Actual Cost from Moves)
            inputs = 0.0
            for move in mo.move_raw_ids:
                inputs += move.product_uom_qty * move.product_id.standard_price

            # 2. 劳动力成本
            labor = 0.0
            if hasattr(mo, 'agri_task_id') and mo.agri_task_id:
                labor = sum(mo.agri_task_id.worklog_ids.mapped(lambda l: l.quantity * (l.employee_id.hourly_cost or 50.0)))

            # 3. 工具与机械成本
            tools = 0.0
            if mo.workorder_ids:
                tools = sum(mo.workorder_ids.mapped(lambda w: (w.duration / 60.0) * w.workcenter_id.costs_hour))

            # 4. 能耗成本
            energy = 0.0
            if hasattr(mo, 'electricity_consumption'):
                energy += mo.electricity_consumption * 1.5
            if hasattr(mo, 'water_consumption'):
                energy += mo.water_consumption * 4.0

            mo.input_cost = inputs
            mo.doer_cost = labor
            mo.tool_cost = tools
            mo.energy_cost = energy
            mo.total_agri_cost = inputs + labor + tools + energy

    # 工时追踪 [US-036-03]
    work_start_datetime = fields.Datetime("Work Start")
    is_working = fields.Boolean("In Progress", default=False)

    # Simplified Approval System [US-039-01]
    approval_state = fields.Selection([
        ('draft', 'Draft'),
        ('to_approve', 'Awaiting Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string="Approval Status", default='draft', tracking=True)

    approver_id = fields.Many2one('res.users', string="Approver", tracking=True)
    approval_date = fields.Datetime("Approval Date", readonly=True)

    simplified_state = fields.Selection([
        ('draft', 'Draft'),
        ('approval', 'Approval'),
        ('ready', 'Ready'),
        ('progress', 'In Progress'),
        ('done', 'Completed'),
    ], string="Simplified State", compute='_compute_simplified_state', store=True, precompute=True)

    # @api.depends(.state., .approval_state.)
    def _compute_simplified_state_old(self):
        for rec in self:
            if rec.state == 'draft' and rec.approval_state == 'draft':
                rec.simplified_state = 'draft'
            elif rec.approval_state == 'to_approve':
                rec.simplified_state = 'approval'
            elif rec.state == 'confirmed' or rec.approval_state == 'approved':
                rec.simplified_state = 'ready'
            elif rec.state == 'progress':
                rec.simplified_state = 'progress'
            elif rec.state in ['to_close', 'done']:
                rec.simplified_state = 'done'
            else:
                rec.simplified_state = 'draft'

    # Drone and spatial audit fields
    actual_flight_area = fields.Float("Actual Flown Area (mu/ha)")
    drone_id = fields.Many2one('maintenance.equipment', string="Drone Used", )

    # 空间审计 [US-053-04]
    out_of_bounds_count = fields.Integer("OOB Point Count", compute='_compute_spatial_audit', help="Number of telemetry points outside the parcel.")
    spatial_compliance_rate = fields.Float("Spatial Compliance (%)", compute='_compute_spatial_audit')

    @api.depends('location_id', 'is_working')
    def _compute_spatial_audit(self):
        """ 统计该任务期间所有 GPS 记录的合规性 """
        for mo in self:
            parcel = mo.location_id
            if not parcel or not hasattr(parcel, 'gps_coordinates') or not parcel.gps_coordinates:
                mo.out_of_bounds_count = 0
                mo.spatial_compliance_rate = 100.0
                continue

            # Create a temporary fence object for boundary check
            if hasattr(self.env['farm.geofence'], 'new'):
                temp_fence = self.env['farm.geofence'].new({
                    'coordinates': parcel.gps_coordinates
                })

                # Get telemetry records during this task
                telemetries = self.env['iiot.telemetry'].search([
                    ('production_id', '=', mo.agri_task_id.id if mo.agri_task_id else False),
                    ('gps_lat', '!=', 0),
                    ('gps_lng', '!=', 0)
                ])

                if not telemetries:
                    mo.out_of_bounds_count = 0
                    mo.spatial_compliance_rate = 100.0
                    continue

                oob_count = 0
                for t in telemetries:
                    if not temp_fence.is_point_inside(t.gps_lng, t.gps_lat):
                        oob_count += 1

                mo.out_of_bounds_count = oob_count
                mo.spatial_compliance_rate = ((len(telemetries) - oob_count) / len(telemetries)) * 100.0
            else:
                # Default values if farm.geofence is not available
                mo.out_of_bounds_count = 0
                mo.spatial_compliance_rate = 100.0

    def action_submit_for_approval(self):
        """Submit intervention for approval"""
        self.ensure_one()
        self.write({'approval_state': 'to_approve'})
        self.message_post(body=_("Intervention submitted for supervisor approval."))

    def action_approve(self):
        """Approve the intervention and confirm in base engine"""
        self.ensure_one()
        self.write({
            'approval_state': 'approved',
            'approver_id': self.env.user.id,
            'approval_date': fields.Datetime.now()
        })
        # Use Base Engine for confirmation
        self.action_confirm_base()
        self.message_post(body=_("Intervention approved by %s") % self.env.user.name)

    def action_reject(self):
        """Reject the intervention"""
        self.ensure_one()
        self.write({'approval_state': 'rejected'})
        self.message_post(body=_("Intervention rejected."))

    def action_start_work(self):
        """Start the actual work via Base Engine (which triggers plugins)"""
        self.ensure_one()
        self.action_start_base()
        self.write({'is_working': True})
        self.message_post(body=_("Labor: Work started at %s") % self.date_start)

    def action_stop_work(self):
        """Stop the actual work via Base Engine"""
        self.ensure_one()
        if not self.date_start:
            return

        self.action_done_base()
        
        if hasattr(self.env['farm.worklog'], 'create'):
            employee = self.env.user.employee_id
            self.env['farm.worklog'].create({
                'employee_id': employee.id if employee else False,
                'task_id': self.agri_task_id.id if self.agri_task_id else False,
                'date': fields.Date.today(),
                'work_type': self.intervention_type or 'harvesting',
                'quantity': 1.0,
                'notes': _('Auto-recorded from intervention %s') % self.name
            })

        self.write({'is_working': False})
        self.message_post(body=_("Labor: Work stopped and recorded at %s") % self.date_finished)

    def action_confirm(self):
        """扩展确认逻辑，通过基础引擎触发合规插件逻辑"""
        # action_confirm_base handles pre_confirm plugins (Compliance check)
        self.filtered(lambda r: r.state == 'draft').action_confirm_base()
        
        # Call the parent method if it exists
        if hasattr(super(AgriInterventionMixin, self), 'action_confirm'):
            return super(AgriInterventionMixin, self).action_confirm()
        return True

    def action_export_drone_kml(self):
        """Export drone route as KML for navigation - US-052-03, US-053-03"""
        """ US-052-03, US-053-03: 将地块边界与周边禁飞区导出为 KML """
        self.ensure_one()
        import base64
        # 1. 查找关联地块
        parcel = self.agri_task_id.land_parcel_id if self.agri_task_id else self.location_dest_id
        if not parcel or not hasattr(parcel, 'gps_coordinates') or not parcel.gps_coordinates:
            raise UserError(_("No GIS boundaries defined for the selected land parcel!"))

        # 2. 查找周边禁飞区围栏
        nearby_fences = self.env['farm.geofence'].search([
            ('fence_type', '=', 'no_fly'),
            ('active', '=', True)
        ])

        # 3. 生成 KML
        kml_header = """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Drone Mission: {name}</name>
    <Style id="workArea"><PolyStyle><color>4d00ff00</color></PolyStyle></Style>
    <Style id="noFly"><PolyStyle><color>4d0000ff</color></PolyStyle></Style>
""".format(name=self.name)

        # 核心作业区
        work_area = f"""    <Placemark>
      <name>Work Area: {parcel.name}</name>
      <styleUrl>#workArea</styleUrl>
      <Polygon><outerBoundaryIs><LinearRing><coordinates>{parcel.gps_coordinates.replace(';', ' ')}</coordinates></LinearRing></outerBoundaryIs></Polygon>
    </Placemark>"""

        # 禁飞区
        nf_areas = ""
        for nf in nearby_fences:
            if hasattr(nf, 'coordinates'):
                nf_areas += f"""    <Placemark>
      <name>NO-FLY: {nf.name}</name>
      <styleUrl>#noFly</styleUrl>
      <Polygon><outerBoundaryIs><LinearRing><coordinates>{nf.coordinates.replace(';', ' ')}</coordinates></LinearRing></outerBoundaryIs></Polygon>
    </Placemark>"""

        kml_footer = """  </Document>
</kml>"""

        full_kml = kml_header + work_area + nf_areas + kml_footer

        # 4. 创建附件
        attachment = self.env['ir.attachment'].create({
            'name': f"{self.name}_mission.kml",
            'type': 'binary',
            'datas': base64.b64encode(full_kml.encode('utf-8')),
            'mimetype': 'application/vnd.google-earth.kml+xml',
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }

    def button_mark_done(self):
        """Extend the done logic to handle drone spraying depletion and graded outputs."""
        for intervention in self:
            # US-052-04: 无人机飞防自动核销
            if hasattr(intervention, 'intervention_type') and intervention.intervention_type == 'aerial_spraying' and intervention.actual_flight_area > 0:
                for move in intervention.move_raw_ids:
                    # 根据实际作业面积动态调整原材料需求量
                    # 假设配方中 product_uom_qty 是针对 1 亩设计的
                    if hasattr(move, 'bom_line_id'):
                        move.product_uom_qty = intervention.actual_flight_area * (move.bom_line_id.product_qty if move.bom_line_id else 1.0)

            if hasattr(intervention, 'intervention_type') and intervention.intervention_type == 'harvesting':
                # Handle graded quantities logic
                total_graded_qty = intervention.grade_a_qty + intervention.grade_b_qty + intervention.grade_c_qty

                if total_graded_qty > 0:
                    # Logic to create separate stock moves and lots for each grade
                    finished_product = intervention.product_id

                    def _create_graded_move_and_lot(grade_type, qty):
                        if qty <= 0:
                            return None

                        # Create a new lot with the specified grade
                        if hasattr(self.env['stock.lot'], 'create'):
                            graded_lot = self.env['stock.lot'].create({
                                'product_id': finished_product.id,
                                'name': finished_product.name + '/' + grade_type.upper() + '/' + (self.env['ir.sequence'].next_by_code('stock.lot') or _('New')),
                                'quality_grade': grade_type,
                            })

                            # Create a stock move for this graded quantity
                            move = self.env['stock.move'].create({
                                'name': _('Harvest Output (%s)') % grade_type.upper(),
                                'product_id': finished_product.id,
                                'product_uom_qty': qty,
                                'product_uom': finished_product.uom_id.id,
                                'location_id': intervention.location_src_id.id, # Production location
                                'location_dest_id': intervention.location_dest_id.id, # Destination (stock) location
                                'production_id': intervention.id,
                                'lot_ids': [(6, 0, [graded_lot.id])] if graded_lot else [],
                                'state': 'done', # Mark as done directly
                            })
                            if hasattr(move, '_action_done'):
                                move._action_done() # Finalize the move
                            return graded_lot.id
                        return None

                    graded_lot_ids = []
                    if hasattr(intervention, 'grade_a_qty'):
                        graded_lot_ids.append(_create_graded_move_and_lot('grade_a', intervention.grade_a_qty))
                    if hasattr(intervention, 'grade_b_qty'):
                        graded_lot_ids.append(_create_graded_move_and_lot('grade_b', intervention.grade_b_qty))
                    if hasattr(intervention, 'grade_c_qty'):
                        graded_lot_ids.append(_create_graded_move_and_lot('grade_c', intervention.grade_c_qty))

                    graded_lot_ids = [lot_id for lot_id in graded_lot_ids if lot_id]

                    # US-005-02: Trigger quality check for custom created graded lots
                    if graded_lot_ids:
                        for lot_id in graded_lot_ids:
                            try:
                                if hasattr(self.env['farm.quality.check'], 'create'):
                                    self.env['farm.quality.check'].create({
                                        'lot_id': lot_id,
                                        'task_id': intervention.agri_task_id.id if intervention.agri_task_id else False,
                                        'name': _('Harvest QC: %s for Grade %s') % (intervention.name, (self.env['stock.lot'].browse(lot_id).quality_grade or 'UNKNOWN').upper()),
                                    })
                            except Exception:
                                pass

                    # Prevent base MRP from creating duplicate finished moves
                    # by setting product_qty to 0 for the super call if custom moves are created
                    intervention.product_qty = 0

                # US-005-02: Trigger quality check for non-graded harvesting
                elif intervention.intervention_type == 'harvesting' and intervention.product_qty > 0:
                    try:
                        if hasattr(intervention.move_finished_ids, 'mapped'):
                            lot_ids = intervention.move_finished_ids.mapped('lot_ids')
                            if hasattr(self.env['farm.quality.check'], 'create') and lot_ids:
                                self.env['farm.quality.check'].create({
                                    'lot_id': lot_ids[:1].id if lot_ids else False,
                                    'task_id': intervention.agri_task_id.id if intervention.agri_task_id else False,
                                    'name': _('Harvest QC: %s') % intervention.name,
                                })
                    except Exception:
                        pass

        # Call super method if available to handle other MRP production logic
        if hasattr(super(AgriInterventionMixin, self), 'button_mark_done'):
            return super(AgriInterventionMixin, self).button_mark_done()
        else:
            # If no parent button_mark_done exists, update state to done
            self.write({'state': 'done'})
            return True