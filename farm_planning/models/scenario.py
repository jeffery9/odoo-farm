from odoo import models, fields, api, _

class AgriScenario(models.Model):
    _name = 'agri.scenario'
    _description = 'Planning Scenario (Simulation)'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Scenario Name", required=True) # e.g., High Yield Scenario 2026
    route_id = fields.Many2one('agri.technical.route', string="Technical Route", required=True)
    planned_area = fields.Float("Planned Area (Hectares)", default=1.0)
    
    # 汇总预测结果
    total_labor_forecast = fields.Float("Total Labor Forecast (Hours)", compute='_compute_forecasts')
    input_forecast_ids = fields.One2many('agri.scenario.input.forecast', 'scenario_id', string="Input Forecasts")

    @api.depends('route_id', 'planned_area')
    def _compute_forecasts(self):
        for scenario in self:
            total_labor = 0.0
            for line in scenario.route_id.line_ids:
                total_labor += (line.template_id.estimated_labor_hours * scenario.planned_area)
            scenario.total_labor_forecast = total_labor

    def action_run_simulation(self):
        """ 运行模拟：根据路线和面积计算投入品需求 """
        self.ensure_one()
        self.input_forecast_ids.unlink()
        forecasts = []
        for line in self.route_id.line_ids:
            for input_line in line.template_id.input_ids:
                forecasts.append((0, 0, {
                    'product_id': input_line.product_id.id,
                    'quantity': input_line.quantity * self.planned_area
                }))
        self.write({'input_forecast_ids': forecasts})
        return True

class AgriScenarioInputForecast(models.Model):
    _name = 'agri.scenario.input.forecast'
    _description = 'Scenario Input Forecast'

    scenario_id = fields.Many2one('agri.scenario', ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Product")
    quantity = fields.Float("Forecasted Quantity")