# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AgriOperationMixin(models.AbstractModel):
    """
    Abstract base model for agricultural process operations and ISA-88 routing phases.
    Provides standard GxP fields, technical manual SOPs, and critical control parameters (CCPs).
    """
    _name = 'agri.operation.mixin'
    _description = 'Agri Process Operation Shared Logic'

    # ISA-88 Agri Activity Type
    agri_activity_type = fields.Selection([
        ('feed', 'Feed / 饲喂工序'),
        ('fertilizer', 'Fertilizer / 施肥工序'),
        ('planting', 'Planting / 种植播种'),
        ('protection', 'Protection / 植保打药'),
        ('processing', 'Processing / 产后加工'),
        ('cleaning', 'CIP/Cleaning / 清洗净化')
    ], string="Agri Activity Type", help="Classify operation as a specific agricultural/processing phase.")

    # Technical instructions (SOP)
    technical_manual = fields.Html(
        string="Technical SOP / 工艺规程",
        help="Detailed standard operating procedure for this specific process step."
    )

    # Critical Control Parameters (CCP)
    param_monitoring_required = fields.Boolean(
        string="Monitor Critical Parameters / 开启关键监控",
        default=False,
        help="Check this if the operation requires strict telemetry monitoring."
    )
    target_value = fields.Float(
        string="Target Parameter Value / 监控目标值",
        help="Theoretical standard/target value for the critical control parameter."
    )
    tolerance_range = fields.Float(
        string="Tolerance (+/-) / 容差范围",
        help="Acceptable deviation above or below the target value."
    )

    # Standard GxP phases
    gxp_phase_type = fields.Selection([
        ('none', 'Standard Execution / 标准执行'),
        ('sterilization', 'Sterilization / 灭菌杀毒'),
        ('fermentation', 'Fermentation / 发酵孵化'),
        ('dehydration', 'Dehydration / 脱水干燥'),
        ('packaging', 'Packaging / 称重包装'),
        ('cip', 'CIP Cleaning / 管道清洗')
    ], string="GxP Phase Type", default="none")
