from odoo import models, fields, api, _

class FarmActivity(models.Model):
    _inherit = 'project.project'

    is_agri_activity = fields.Boolean(
        string="Is Agricultural Activity", 
        default=False,
        help="Mark this project as an agricultural activity to enable specialized features."
    )
    
    activity_family = fields.Selection([
        ('planting', 'Planting'),
        ('livestock', 'Livestock'),
        ('aquaculture', 'Aquaculture'),
        ('agritourism', 'Agritourism'),
        ('baking', 'Baking'),
        ('winemaking', 'Winemaking'),
        ('food_processing', 'Food Processing'),
    ], string="Activity Family", help="Specify the agricultural sector.")

    production_cycle = fields.Selection([
        ('annual', 'Annual'),
        ('perennial', 'Perennial'),
    ], string="Production Cycle", default='annual')

    task_sequence_id = fields.Many2one(
        'ir.sequence', 
        string="Task Sequence",
        help="Custom sequence for tasks in this project. If empty, the family default will be used."
    )

class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('project_id'):
                project = self.env['project.project'].browse(vals['project_id'])
                if project.is_agri_activity:
                    # 获取序列号规则 [US-01-01]
                    sequence = project.task_sequence_id
                    if not sequence and project.activity_family:
                        seq_code = 'farm.task.%s' % project.activity_family
                        sequence = self.env['ir.sequence'].search([('code', '=', seq_code)], limit=1)
                    
                    if sequence:
                        vals['name'] = (sequence.next_by_id() or '') + ' - ' + (vals.get('name') or '')
        return super().create(vals_list)
