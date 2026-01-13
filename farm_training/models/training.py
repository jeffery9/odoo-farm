from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class FarmCertificateType(models.Model):
    _name = 'farm.certificate.type'
    _description = 'Agricultural Certificate Type'

    name = fields.Char("Certificate Name", required=True, translate=True) # e.g. "Drone Operator License"
    code = fields.Char("Code", required=True)
    required_for_intervention_types = fields.Selection([
        ('protection', 'Crop Protection (飞防/植保)'),
        ('medical', 'Medical/Prevention (防疫)'),
        ('harvesting', 'Mechanical Harvesting (机收)')
    ], string="Mandatory for Task Type", help="If set, system will check for this certificate during task confirmation.")

class FarmCertificate(models.Model):
    _name = 'farm.certificate'
    _description = 'Farmer Certificate'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Certificate No.", required=True)
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    certificate_type_id = fields.Many2one('farm.certificate.type', string="Type", required=True)
    issue_date = fields.Date("Issue Date")
    expiry_date = fields.Date("Expiry Date")
    is_valid = fields.Boolean("Is Valid", compute='_compute_is_valid', store=True)
    attachment_ids = fields.Many2many('ir.attachment', string="Certificate Photos")

    @api.depends('expiry_date')
    def _compute_is_valid(self):
        today = fields.Date.today()
        for rec in self:
            rec.is_valid = not rec.expiry_date or rec.expiry_date >= today

class FarmTrainingSession(models.Model):
    _name = 'farm.training.session'
    _description = 'Farmer Training Session'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Topic", required=True)
    date = fields.Date("Date", default=fields.Date.today)
    hours = fields.Float("Duration (Hours)")
    trainer_id = fields.Many2one('res.partner', string="Trainer/Expert")
    trainee_ids = fields.Many2many('hr.employee', string="Trainees")
    content = fields.Html("Training Content")
    state = fields.Selection([('draft', 'Draft'), ('done', 'Completed')], default='draft')

    def action_complete(self):
        self.write({'state': 'done'})

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    certificate_ids = fields.One2many('farm.certificate', 'employee_id', string="Certificates")
    training_session_ids = fields.Many2many('farm.training.session', string="Training History")
    total_training_hours = fields.Float("Total Training Hours", compute='_compute_training_hours')

    def _compute_training_hours(self):
        for emp in self:
            emp.total_training_hours = sum(emp.training_session_ids.filtered(lambda s: s.state == 'done').mapped('hours'))

class AgriIntervention(models.Model):
    _inherit = 'mrp.production'

    def action_confirm(self):
        """ 
        US-17-08: 资质准入检查逻辑 
        如果该干预任务类型需要特殊资质，检查执行人是否持证
        """
        for mo in self:
            # 1. 查找此任务类型是否需要证书
            required_cert_type = self.env['farm.certificate.type'].search([
                ('required_for_intervention_types', '=', mo.intervention_type)
            ], limit=1)

            if required_cert_type:
                # 2. 检查所有执行人 (doer_ids 来自 farm_operation)
                if not mo.doer_ids:
                    raise UserError(_("This task (%s) requires certified personnel, but no workers are assigned.") % mo.intervention_type)
                
                for employee in mo.doer_ids:
                    valid_cert = employee.certificate_ids.filtered(
                        lambda c: c.certificate_type_id == required_cert_type and c.is_valid
                    )
                    if not valid_cert:
                        raise UserError(_("ACCESS DENIED: Worker %s does not have a valid '%s' for this %s task.") % (
                            employee.name, required_cert_type.name, mo.intervention_type
                        ))
        
        return super(AgriIntervention, self).action_confirm()