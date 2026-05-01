from odoo import fields, models, api, _

class IndustryTaskTemplate(models.Model):
    """Task template data for industry packages"""
    _name = 'farm.industry.task.template'
    _description = 'Industry Package Task Template Data'

    package_id = fields.Many2one(
        'agri.industry.data.package',
        string="Industry Package",
        required=True,
        ondelete='cascade'
    )

    name = fields.Char("Template Name", required=True)
    description = fields.Text("Description")
    fold = fields.Boolean("Folded in Kanban", default=False)
    project_id = fields.Many2one('project.project', string="Project")

    # Additional fields for agricultural task templates
    expected_duration = fields.Integer("Expected Duration (Days)")
    required_equipment = fields.Char("Required Equipment")
    required_inputs = fields.Char("Required Inputs")