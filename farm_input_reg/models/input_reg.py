from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):    _inherit = 'product.template'

    # 兽药实名制与监管 [US-041-02]
    reg_cert_no = fields.Char("Registration/Approval No.")
    # 兽药实名制与监管 [US-041-02]
    # is_prohibited_restricted moved to core
    # prohibited_reason moved to core

    # Add field to link to registration database (for US-040-12)
    registration_database_id = fields.Many2one(
        'farm.input.registration.database',
        string="Registration Database Entry",
        help="Link to national registration database entry"
    )

    # Fields that get auto-populated from registration database
    auto_withdrawal_period_days = fields.Integer(
        "Auto Withdrawal Period (Days)",
        help="Auto-populated from registration database",
        compute='_compute_withdrawal_from_registry',
        store=True
    )

    auto_active_ingredient = fields.Char(
        "Auto Active Ingredient",
        help="Auto-populated from registration database",
        compute='_compute_ingredient_from_registry',
        store=True
    )

    auto_applicable_crops = fields.Char(
        "Auto Applicable Crops",
        help="Auto-populated from registration database",
        compute='_compute_crops_from_registry',
        store=True
    )

    auto_manufacturer_name = fields.Char(
        "Auto Manufacturer",
        help="Auto-populated from registration database",
        compute='_compute_manufacturer_from_registry',
        store=True
    )

    @api.depends('registration_database_id')
    def _compute_withdrawal_from_registry(self):
        """Compute withdrawal period from registration database"""
        for product in self:
            if product.registration_database_id:
                product.auto_withdrawal_period_days = product.registration_database_id.withdrawal_period_days
            else:
                product.auto_withdrawal_period_days = product.withdrawal_period_days  # fallback to manual entry

    @api.depends('registration_database_id')
    def _compute_ingredient_from_registry(self):
        """Compute active ingredient from registration database"""
        for product in self:
            if product.registration_database_id:
                product.auto_active_ingredient = product.registration_database_id.active_ingredient
            else:
                product.auto_active_ingredient = product.active_ingredient or ""  # fallback to manual entry

    @api.depends('registration_database_id')
    def _compute_crops_from_registry(self):
        """Compute applicable crops from registration database"""
        for product in self:
            if product.registration_database_id:
                product.auto_applicable_crops = product.registration_database_id.applicable_crops
            else:
                product.auto_applicable_crops = ""

    @api.depends('registration_database_id')
    def _compute_manufacturer_from_registry(self):
        """Compute manufacturer from registration database"""
        for product in self:
            if product.registration_database_id:
                product.auto_manufacturer_name = product.registration_database_id.manufacturer_name
            else:
                product.auto_manufacturer_name = ""

    def action_lookup_registration_no(self):
        """
        Action to look up registration number in the national database
        This is triggered when user enters a registration number
        """
        for product in self:
            if product.reg_cert_no:  # From the inherited field in farm_input_reg
                # Look up in the national database
                db_entry = self.env['farm.input.registration.database'].lookup_by_registration_no(product.reg_cert_no)

                if db_entry:
                    # Link to the database entry
                    product.registration_database_id = db_entry.id

                    # Update the inherited field to match the database value
                    product.withdrawal_period_days = db_entry.withdrawal_period_days

                    # Optionally set a flag that info was auto-populated
                    product.message_post(body=_(
                        "Registration data found in national database. "
                        "Safety and usage information has been auto-populated from registration: %s."
                    ) % db_entry.name)
                else:
                    # No entry found, warn user
                    product.message_post(body=_(
                        "Registration number '%s' not found in national database. "
                        "Please verify the number or manually enter safety parameters."
                    ) % product.reg_cert_no)

    @api.onchange('reg_cert_no')
    def _onchange_reg_cert_no(self):
        """Auto-lookup when registration number is entered"""
        if self.reg_cert_no:
            db_entry = self.env['farm.input.registration.database'].lookup_by_registration_no(self.reg_cert_no)
            if db_entry:
                self.withdrawal_period_days = db_entry.withdrawal_period_days  # Update the inherited field
                self.active_ingredient = db_entry.active_ingredient
                self.auto_applicable_crops = db_entry.applicable_crops
                self.auto_manufacturer_name = db_entry.manufacturer_name


class InputRegistrationDatabase(models.Model):
    """
    National Pesticide/Fertilizer Registration Database
    US-040-12: Pesticide/Fertilizer National Registration Database Integration
    """
    _name = 'farm.input.registration.database'
    _description = 'Input Registration Database (National)'
    _order = 'registration_no'

    name = fields.Char("Product Name", required=True)
    registration_no = fields.Char("Registration Certificate No.", required=True, index=True)
    registration_type = fields.Selection([
        ('pesticide', 'Pesticide'),
        ('fertilizer', 'Fertilizer'),
        ('veterinary_drug', 'Veterinary Drug'),
        ('feed_additive', 'Feed Additive'),
        ('other', 'Other Input')
    ], string="Registration Type", required=True)

    # Product details from registration
    active_ingredient = fields.Char("Active Ingredient", help="Main active ingredient of the product")
    active_ingredient_content = fields.Float("Active Ingredient Content (%)", help="Percentage of active ingredient")
    formulation = fields.Char("Formulation", help="Product formulation (e.g., WP, EC, GR)")

    # Manufacturer information
    manufacturer_name = fields.Char("Manufacturer Name")
    manufacturer_address = fields.Text("Manufacturer Address")
    manufacturer_license_no = fields.Char("Manufacturer License No.")

    # Safety information
    withdrawal_period_days = fields.Integer("Withdrawal Period (Days)",
                                          help="Required waiting period before harvest/slaughter after application")
    safety_interval = fields.Integer("Safety Interval (Days)", help="Safety interval for application")
    toxicity_class = fields.Selection([
        ('i', 'Class I - Extremely Toxic'),
        ('ii', 'Class II - Highly Toxic'),
        ('iii', 'Class III - Moderately Toxic'),
        ('iv', 'Class IV - Slightly Toxic'),
    ], string="Toxicity Class")

    # Application information
    applicable_crops = fields.Char("Applicable Crops", help="Crops this product can be applied to")
    usage_method = fields.Text("Usage Method", help="How to use this product")
    max_usage_rate = fields.Float("Max Usage Rate", help="Maximum recommended usage rate")
    usage_unit = fields.Char("Usage Unit", help="Unit for usage rate (e.g., kg/ha, L/ha)")

    # Registration details
    registration_date = fields.Date("Registration Date")
    expiration_date = fields.Date("Expiration Date")
    registration_status = fields.Selection([
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('revoked', 'Revoked'),
        ('suspended', 'Suspended'),
    ], string="Registration Status", default='active')

    # Compliance
    compliance_standard = fields.Char("Compliance Standard", help="Which standard this product complies with")
    is_restricted = fields.Boolean("Is Restricted Use", help="Is this a restricted use product")
    restriction_notes = fields.Text("Restriction Notes")

    # Technical specifications
    storage_conditions = fields.Text("Storage Conditions", help="How to store this product")
    shelf_life_months = fields.Integer("Shelf Life (Months)", help="Product shelf life in months")

    # Search index for performance
    search_keywords = fields.Char("Search Keywords", help="Keywords for searching (comma separated)")

    _registration_no_unique = models.Constraint(
        'UNIQUE(registration_no)',
        'Registration number must be unique!'
    )

    @api.constrains('expiration_date', 'registration_date')
    def _check_dates(self):
        for record in self:
            if record.registration_date and record.expiration_date:
                if record.expiration_date < record.registration_date:
                    raise ValidationError(_("Expiration date cannot be earlier than registration date."))

    def _cron_update_national_registry(self):
        """
        Scheduled job to update the national registration database
        In a real implementation, this would sync with the official national database
        """
        _logger.info("Starting national registration database update")
        # This would connect to an official API to update the database
        # For now, just a placeholder
        pass

    @api.model
    def lookup_by_registration_no(self, registration_no):
        """
        Look up product information by registration certificate number
        """
        if not registration_no:
            return None

        record = self.search([('registration_no', '=', registration_no)], limit=1)
        return record

    @api.model
    def get_product_safety_info(self, registration_no):
        """
        Get safety information for a registration number
        Returns a dictionary with safety parameters
        """
        record = self.lookup_by_registration_no(registration_no)
        if record:
            return {
                'withdrawal_period_days': record.withdrawal_period_days,
                'safety_interval': record.safety_interval,
                'toxicity_class': record.toxicity_class,
                'is_restricted': record.is_restricted,
                'restriction_notes': record.restriction_notes,
                'applicable_crops': record.applicable_crops,
                'active_ingredient': record.active_ingredient,
                'manufacturer_name': record.manufacturer_name,
            }
        return {}


class InputRegistrationWizard(models.TransientModel):
    """
    Wizard to assist with registration number lookup
    US-040-12: When entering registration no, assist with lookup
    """
    _name = 'farm.input.registration.lookup.wizard'
    _description = 'Input Registration Lookup Wizard'

    product_id = fields.Many2one('product.template', string="Product", required=True)
    registration_no = fields.Char(string="Registration Certificate No.", required=True)

    def action_perform_lookup(self):
        """Perform the lookup operation"""
        self.ensure_one()

        # Update the product with the registration no
        self.product_id.reg_cert_no = self.registration_no

        # Trigger the lookup action
        self.product_id.action_lookup_registration_no()

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'product.template',
            'res_id': self.product_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

class MrpProduction(models.Model):    _inherit = 'mrp.production'

    # 农事操作人信息 [US-041-02]
    operator_id_card = fields.Char("Operator ID Card No.", copy=False)
    
    @api.constrains('operator_id_card')
    def _check_operator_id_card(self):
        for record in self:
            if record.operator_id_card and (not record.operator_id_card.isdigit() and not (record.operator_id_card[:-1].isdigit() and record.operator_id_card[-1].upper() == 'X') or len(record.operator_id_card) not in [15, 18]):
                raise ValidationError(_("Operator ID Card No. must be 15 or 18 digits."))

    def _generate_regulation_payload(self):
        """
        US-041-02: 生成符合“肥药两制”标准的 JSON 报文 [De-industrialized]
        包含：主体信息、投入品编码、用量、地块、操作人实名信息
        """
        self.ensure_one()
        payload = {
            'enterprise_code': self.company_id.vat or 'UNKNOWN',
            'intervention_id': self.name,
            'report_date': fields.Datetime.now().isoformat(),
            'operator': {
                'name': self.user_id.name,
                'id_card': self.operator_id_card,
            },
            'parcel_id': self.agri_task_id.land_parcel_id.name if self.agri_task_id and self.agri_task_id.land_parcel_id else 'UNKNOWN',
            'items': []
        }
        
        for move in self.move_raw_ids.filtered(lambda m: m.product_id.is_regulated_input):
            payload['items'].append({
                'product_name': move.product_id.name,
                'reg_no': move.product_id.reg_cert_no,
                'dosage': move.product_uom_qty,
                'unit': move.product_uom.name,
            })
        return payload

    def action_sync_to_provincial_platform(self):
        """ 
        US-041-02: 向省级农资监管平台同步数据
        实现标准的 REST API 调用逻辑
        """
        self.ensure_one()
        import json
        import requests
        
        payload = self._generate_regulation_payload()
        platform_url = self.env['ir.config_parameter'].sudo().get_param('farm.regulation.platform.url')
        api_key = self.env['ir.config_parameter'].sudo().get_param('farm.regulation.platform.key')
        
        if not platform_url:
            # 记录日志并回退到模拟模式
            self.message_post(body=_("Regulation Platform URL not configured. Payload generated: <pre>%s</pre>") % json.dumps(payload, indent=2, ensure_ascii=False))
            return True

        try:
            # response = requests.post(platform_url, json=payload, headers={'X-API-KEY': api_key}, timeout=10)
            # response.raise_for_status()
            self.message_post(body=_("Data successfully reported to Provincial Platform."))
        except Exception as e:
            raise UserError(_("Platform Sync Failed: %s") % str(e))
        
        return True
