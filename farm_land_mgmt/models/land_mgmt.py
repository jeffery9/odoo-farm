from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class FarmLocation(models.Model):
    _inherit = 'stock.location'

    # 土地承包权信息 [US-65]
    land_contract_no = fields.Char("Land Contract No. (承包经营权证号)")
    contractor_id = fields.Many2one('res.partner', string="Contractor (承包方)")
    
    # 土地性质 [US-65]
    land_nature = fields.Selection([
        ('general_farmland', '一般农田'),
        ('permanent_basic_farmland', '永久基本农田'),
        ('construction_land', '建设用地'),
        ('other', '其他')
    ], string="Land Nature (土地性质)", default='general_farmland')

    @api.constrains('land_nature', 'is_land_parcel')
    def _check_land_nature_validity(self):
        for record in self:
            if record.is_land_parcel and record.land_nature == 'construction_land':
                raise ValidationError(_("Land marked as 'Construction Land' cannot be a 'Land Parcel'."))

class FarmActivity(models.Model):
    _inherit = 'project.project'

    @api.constrains('activity_family', 'land_parcel_ids')
    def _check_activity_land_use_compliance(self):
        for record in self:
            if record.activity_family in ['aquaculture', 'agritourism'] and record.land_parcel_ids:
                for parcel in record.land_parcel_ids:
                    if parcel.land_nature == 'permanent_basic_farmland':
                        raise ValidationError(_("Activity Type '%s' is not allowed on 'Permanent Basic Farmland' for parcel '%s'.") % (record.activity_family, parcel.name))

class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.constrains('land_parcel_id', 'project_id')
    def _check_task_land_use_compliance(self):
        for record in self:
            if record.project_id and record.land_parcel_id:
                record.project_id._check_activity_land_use_compliance()
