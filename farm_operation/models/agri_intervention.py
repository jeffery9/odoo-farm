from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AgriIntervention(models.Model):
    _inherit = 'mrp.production'
    _description = 'Agricultural Intervention (De-industrialized View)'

    agri_task_id = fields.Many2one(
        'project.task',
        string="Production Task",
        help="The specific production task this intervention belongs to."
    )
    
    # 农业特有的作业分类 [核心字段 - 已恢复]
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

    def action_export_drone_kml(self):
        """ US-22-03, US-23-03: 将地块边界与周边禁飞区导出为 KML """
        self.ensure_one()
        import base64
        # 1. 查找关联地块
        parcel = self.agri_task_id.land_parcel_id or self.location_dest_id
        if not parcel or not parcel.gps_coordinates:
            raise UserError(_("No GIS boundaries defined for the selected land parcel!"))
        
        # 2. 查找周边禁飞区围栏
        nearby_fences = self.env['farm.geofence'].search([
            ('fence_type', '=', 'no_fly'),
            ('active', '=', True)
        ])
        
        # 3. 生成 KML
        kml_header = """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<kml xmlns=\"http://www.opengis.net/kml/2.2\">
  <Document>
    <name>Drone Mission: {name}</name>
    <Style id=\"workArea\"><PolyStyle><color>4d00ff00</color></PolyStyle></Style>
    <Style id=\"noFly\"><PolyStyle><color>4d0000ff</color></PolyStyle></Style>
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

    # Ekylibre Mapping: Intervention Parameters [US-Mapping]
    doer_ids = fields.Many2many('hr.employee', string="Doers/Workers")
    tool_ids = fields.Many2many('maintenance.equipment', string="Tools/Machinery")
    
    procedure_name = fields.Char("Procedure/Method", help="e.g. Mechanical sowing, manual weeding")

    # Harvest Grading [US-02-04]
    grade_a_qty = fields.Float("Grade A Quantity")
    grade_b_qty = fields.Float("Grade B Quantity")
    grade_c_qty = fields.Float("Grade C Quantity")

    @api.constrains('grade_a_qty', 'grade_b_qty', 'grade_c_qty')
    def _check_graded_quantities(self):
        for intervention in self:
            if intervention.intervention_type == 'harvesting' and (intervention.grade_a_qty < 0 or intervention.grade_b_qty < 0 or intervention.grade_c_qty < 0):
                raise UserError(_("Graded quantities cannot be negative."))

    # Ekylibre Mapping: Costing [US-Mapping]
    input_cost = fields.Float("Input Cost", compute='_compute_agri_costs', store=True)
    tool_cost = fields.Float("Tool/Machinery Cost", compute='_compute_agri_costs', store=True)
    doer_cost = fields.Float("Labor Cost", compute='_compute_agri_costs', store=True)
    total_agri_cost = fields.Float("Total Intervention Cost", compute='_compute_agri_costs', store=True)

    # US-02-03: Soil Nutrient Inputs
    pure_n_qty = fields.Float("Pure Nitrogen (N) kg", compute='_compute_agri_costs', store=True)
    pure_p_qty = fields.Float("Pure Phosphorus (P) kg", compute='_compute_agri_costs', store=True)
    pure_k_qty = fields.Float("Pure Potassium (K) kg", compute='_compute_agri_costs', store=True)

    @api.depends('move_raw_ids.state', 'move_raw_ids.product_uom_qty', 'workorder_ids.duration')
    def _compute_agri_costs(self):
        for mo in self:
            # 1. 投入品成本与养分计算
            inputs = 0.0
            n_total = p_total = k_total = 0.0
            for move in mo.move_raw_ids:
                inputs += move.product_uom_qty * move.product_id.standard_price
                # 计算养分 (假设 UOM 是 kg)
                n_total += move.product_uom_qty * (move.product_id.n_content / 100.0)
                p_total += move.product_uom_qty * (move.product_id.p_content / 100.0)
                k_total += move.product_uom_qty * (move.product_id.k_content / 100.0)
            
            # 2. 劳动力成本
            labor = sum(mo.workorder_ids.mapped('duration')) / 60.0 * 50.0 # 假设 50
            
            # 3. 工具与机械成本
            tools = sum(mo.workorder_ids.mapped(lambda w: w.duration / 60.0 * w.workcenter_id.costs_hour))
            
            # US-22-05: 累加无人机作业成本 (基于作业亩数 * 耗能)
            if mo.intervention_type == 'aerial_spraying' and mo.drone_id:
                # 假设每亩综合成本 5.0 (折旧+电池损耗)
                tools += mo.actual_flight_area * 5.0
            
            mo.input_cost = inputs
            mo.doer_cost = labor
            mo.tool_cost = tools
            mo.total_agri_cost = inputs + labor + tools
            mo.pure_n_qty = n_total
            mo.pure_p_qty = p_total
            mo.pure_k_qty = k_total

    # 工时追踪 [US-13-03]
    work_start_datetime = fields.Datetime("Work Start")
    is_working = fields.Boolean("In Progress", default=False)

    def action_start_work(self):
        """ 一键打卡：开始作业 """
        # US-02-06: Weather window check for spray operations
        if self.intervention_type in ['fertilizing', 'protection', 'aerial_spraying']:
            self._check_weather_window()

        self.ensure_one()
        self.write({
            'work_start_datetime': fields.Datetime.now(),
            'is_working': True
        })
        self.message_post(body=_("Labor: Work started at %s") % self.work_start_datetime)

    def _check_weather_window(self):
        """
        Check weather conditions before allowing spray operations [US-02-06]
        """
        self.ensure_one()

        # 获取作业地点最近的天气预报
        parcel = self.agri_task_id.land_parcel_id
        if not parcel or not parcel.gps_coordinates:
            return  # 如果没有地理信息，则跳过检查

        # 获取未来24小时天气预报
        from datetime import datetime, timedelta
        end_time = datetime.now() + timedelta(hours=24)

        # 查找相关的天气预报记录 (需要安装天气模块)
        if hasattr(self.env['farm.weather.forecast'], 'search'):
            forecast = self.env['farm.weather.forecast'].search([
                ('location_id', '=', parcel.id),
                ('forecast_datetime', '<=', end_time),
                ('forecast_datetime', '>=', datetime.now()),
                ('forecast_datetime', '=', datetime.now())  # 最近的预报
            ], limit=1, order='forecast_datetime asc')

            if forecast:
                # 检查风速是否超过4级（限制喷洒作业）
                if forecast.wind_speed_kmh and forecast.wind_speed_kmh > 16:  # 4级风约16km/h
                    # 创建审批Activity
                    self.activity_schedule(
                        'mail.mail_activity_data_todo',
                        summary=_('Weather Window Check: Wind too strong for spray operation [%s km/h]') % forecast.wind_speed_kmh,
                        note=_('Attempted spray operation on %s was blocked due to high wind speed (%s km/h > 16 km/h). '
                               'Please verify with technical director before proceeding with spray operation.') % (
                                   self.name, forecast.wind_speed_kmh
                               ),
                        user_id=self.user_id.id
                    )
                    raise UserError(_(
                        "WEATHER WINDOW BLOCK: Wind speed too high for spray operation. "
                        "Current wind speed is %s km/h, maximum allowed is 16 km/h (4 level wind). "
                        "An exception handling task has been automatically created for technical director review."
                    ) % forecast.wind_speed_kmh)

    def action_stop_work(self):
        """ 一键打卡：停止作业并自动创建工时记录 """
        self.ensure_one()
        if not self.work_start_datetime:
            return
            
        now = fields.Datetime.now()
        if hasattr(self.env['farm.worklog'], 'create'):
            employee = self.env.user.employee_id
            self.env['farm.worklog'].create({
                'employee_id': employee.id if employee else False,
                'task_id': self.agri_task_id.id,
                'date': fields.Date.today(),
                'work_type': self.intervention_type or 'harvesting',
                'quantity': 1.0, 
                'notes': _('Auto-recorded from intervention %s') % self.name
            })
            
        self.write({
            'is_working': False,
            'work_start_datetime': False
        })
        self.message_post(body=_("Labor: Work stopped and recorded at %s") % now)

    def action_confirm(self):
        """ 扩展确认逻辑，进行安全拦截 [US-03-04] 并传递任务 ID 到供应端 [US-03-02] """
        for mo in self:
            # 1. 检查有机拦截
            is_organic_parcel = mo.agri_task_id.land_parcel_id.certification_level in ['organic', 'organic_transition']
            for move in mo.move_raw_ids:
                if move.product_id.is_agri_input and not move.product_id.is_safety_approved:
                    if is_organic_parcel:
                        # 如果是有机地块，记录违规日期以重置转换期 [US-12-02]
                        mo.agri_task_id.land_parcel_id.last_prohibited_substance_date = fields.Date.today()
                        # 发出警告而非强制报错，这里选择报错以严格合规
                        raise UserError(_("COMPLIANCE ERROR: Product %s is not approved for organic production on parcel %s!") % (
                            move.product_id.name, mo.agri_task_id.land_parcel_id.name
                        ))
            
            # 2. 传递 agri_task_id 到采购逻辑 (通过 procurement_group)
            if mo.agri_task_id and mo.procurement_group_id:
                mo.procurement_group_id.agri_task_id = mo.agri_task_id.id

            # 3. 触发休药期更新 (调用 farm_safety 注入的方法)
            if hasattr(mo.agri_task_id, 'action_confirm_intervention_safety'):
                mo.agri_task_id.action_confirm_intervention_safety(mo.move_raw_ids.mapped('product_id').ids)
                
        return super(AgriIntervention, self).action_confirm()

    actual_flight_area = fields.Float("Actual Flown Area (mu/ha)")
    drone_id = fields.Many2one('maintenance.equipment', string="Drone Used", domain="[('is_drone', '=', True)]")
    
    # 空间审计 [US-23-04]
    out_of_bounds_count = fields.Integer("OOB Point Count", compute='_compute_spatial_audit', help="Number of telemetry points outside the parcel.")
    spatial_compliance_rate = fields.Float("Spatial Compliance (%)", compute='_compute_spatial_audit')

    @api.depends('agri_task_id.land_parcel_id', 'is_working')
    def _compute_spatial_audit(self):
        """ 统计该任务期间所有 GPS 记录的合规性 """
        for mo in self:
            parcel = mo.agri_task_id.land_parcel_id
            if not parcel or not parcel.gps_coordinates:
                mo.out_of_bounds_count = 0
                mo.spatial_compliance_rate = 100.0
                continue
            
            # 创建一个临时围栏对象进行判定
            temp_fence = self.env['farm.geofence'].new({
                'coordinates': parcel.gps_coordinates
            })
            
            # 获取该任务期间的遥测记录
            telemetries = self.env['farm.telemetry'].search([
                ('production_id', '=', mo.agri_task_id.id),
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

    def button_mark_done(self):
        """ Extend the done logic to handle drone spraying depletion and graded outputs. """
        for intervention in self:
            # US-22-04: 无人机飞防自动核销
            if intervention.intervention_type == 'aerial_spraying' and intervention.actual_flight_area > 0:
                for move in intervention.move_raw_ids:
                    # 根据实际作业面积动态调整原材料需求量
                    # 假设配方中 product_uom_qty 是针对 1 亩设计的
                    move.product_uom_qty = intervention.actual_flight_area * (move.bom_line_id.product_qty if move.bom_line_id else 1.0)

            if intervention.intervention_type == 'harvesting':
                # Handle graded quantities logic
                total_graded_qty = intervention.grade_a_qty + intervention.grade_b_qty + intervention.grade_c_qty
                
                if total_graded_qty > 0:
                    # Logic to create separate stock moves and lots for each grade
                    finished_product = intervention.product_id
                    
                    def _create_graded_move_and_lot(grade_type, qty):
                        if qty <= 0:
                            return None
                        
                        # Create a new lot with the specified grade
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
                            'lot_ids': [(6, 0, [graded_lot.id])],
                            'state': 'done', # Mark as done directly
                        })
                        move._action_done() # Finalize the move
                        return graded_lot.id
                        
                    graded_lot_ids = []
                    graded_lot_ids.append(_create_graded_move_and_lot('grade_a', intervention.grade_a_qty))
                    graded_lot_ids.append(_create_graded_move_and_lot('grade_b', intervention.grade_b_qty))
                    graded_lot_ids.append(_create_graded_move_and_lot('grade_c', intervention.grade_c_qty))
                    
                    graded_lot_ids = [lot_id for lot_id in graded_lot_ids if lot_id]

                    # US-05-02: Trigger quality check for custom created graded lots
                    if graded_lot_ids:
                        for lot_id in graded_lot_ids:
                            try:
                                self.env['farm.quality.check'].create({
                                    'lot_id': lot_id,
                                    'task_id': intervention.agri_task_id.id,
                                    'name': _('Harvest QC: %s for Grade %s') % (intervention.name, self.env['stock.lot'].browse(lot_id).quality_grade.upper()),
                                })
                            except Exception:
                                pass

                    # Prevent base MRP from creating duplicate finished moves
                    # by setting product_qty to 0 for the super call if custom moves are created
                    intervention.product_qty = 0

            # US-05-02: Trigger quality check for non-graded harvesting
            elif intervention.intervention_type == 'harvesting' and intervention.product_qty > 0:
                try:
                    lot_ids = intervention.move_finished_ids.mapped('lot_ids')
                    self.env['farm.quality.check'].create({
                        'lot_id': lot_ids[:1].id if lot_ids else False,
                        'task_id': intervention.agri_task_id.id,
                        'name': _('Harvest QC: %s') % intervention.name,
                    })
                except Exception:
                    pass 

        # Call super method to handle other MRP production logic (e.g., raw material consumption, state change)
        res = super(AgriIntervention, self).button_mark_done()
        return res

class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'

    agri_task_id = fields.Many2one('project.task', string="Agri Task")