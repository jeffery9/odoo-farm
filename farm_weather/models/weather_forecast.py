from odoo import models, fields, api, _
import requests
import logging

_logger = logging.getLogger(__name__)

class FarmWeatherForecast(models.Model):
    _name = 'farm.weather.forecast'
    _description = 'Farm Weather Forecast'
    _order = 'date asc'

    date = fields.Date("Date", required=True)
    location_id = fields.Many2one('stock.location', string="Farm Location", domain=[('is_land_parcel', '=', True)])
    
    temp_max = fields.Float("Max Temp (℃)")
    temp_min = fields.Float("Min Temp (℃)")
    precipitation = fields.Float("Precipitation (mm)")
    condition = fields.Char("Condition") # e.g., Sunny, Cloudy, Rainy
    icon = fields.Char("Icon ID")
    
    humidity = fields.Float("Humidity (%)")
    wind_speed = fields.Float("Wind Speed (m/s)")
    
    is_warning = fields.Boolean("Weather Warning", compute='_compute_warning', store=True)
    warning_type = fields.Selection([
        ('frost', 'Frost Risk (霜冻)'),
        ('storm', 'Heavy Rain/Storm (大雨/暴雨)'),
        ('heat', 'Extreme Heat (高温)'),
        ('wind', 'Strong Wind (大风)')
    ], string="Warning Type")

    @api.depends('temp_min', 'precipitation', 'temp_max', 'wind_speed')
    def _compute_warning(self):
        for record in self:
            warning = False
            w_type = False
            if record.temp_min < 0:
                warning = True
                w_type = 'frost'
            elif record.precipitation > 50:
                warning = True
                w_type = 'storm'
            elif record.temp_max > 38:
                warning = True
                w_type = 'heat'
            elif record.wind_speed > 15:
                warning = True
                w_type = 'wind'
            
            record.is_warning = warning
            record.warning_type = w_type

    @api.model
    def action_fetch_weather_all_locations(self):
        """ Cron Job to fetch weather for all locations with GIS coordinates """
        locations = self.env['stock.location'].search([
            ('is_land_parcel', '=', True),
            ('gps_lat', '!=', 0),
            ('gps_lng', '!=', 0)
        ])
        for loc in locations:
            self._fetch_weather_for_location(loc)

    def _fetch_weather_for_location(self, location):
        """ 
        Call external Weather API (Example: OpenWeatherMap OneCall API)
        Note: In real production, use the configured API Key.
        """
        api_key = self.env['ir.config_parameter'].sudo().get_param('farm_weather.api_key')
        if not api_key:
            _logger.warning("Weather API Key not configured.")
            return

        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={location.gps_lat}&lon={location.gps_lng}&appid={api_key}&units=metric"
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                # Process 5-day / 3-hour forecast (simplified to daily for the model)
                forecasts_by_date = {}
                for entry in data.get('list', []):
                    dt = fields.Date.to_date(entry['dt_txt'])
                    if dt not in forecasts_by_date:
                        forecasts_by_date[dt] = {
                            'temp_max': entry['main']['temp_max'],
                            'temp_min': entry['main']['temp_min'],
                            'precipitation': entry.get('rain', {}).get('3h', 0) + entry.get('snow', {}).get('3h', 0),
                            'condition': entry['weather'][0]['main'],
                            'icon': entry['weather'][0]['icon'],
                            'humidity': entry['main']['humidity'],
                            'wind_speed': entry['wind']['speed'],
                        }
                    else:
                        f = forecasts_by_date[dt]
                        f['temp_max'] = max(f['temp_max'], entry['main']['temp_max'])
                        f['temp_min'] = min(f['temp_min'], entry['main']['temp_min'])
                        f['precipitation'] += entry.get('rain', {}).get('3h', 0) + entry.get('snow', {}).get('3h', 0)

                # Update or create records
                for dt, vals in forecasts_by_date.items():
                    existing = self.search([('date', '=', dt), ('location_id', '=', location.id)], limit=1)
                    if existing:
                        existing.write(vals)
                    else:
                        vals.update({'date': dt, 'location_id': location.id})
                        self.create(vals)
            else:
                _logger.error(f"Weather API Error: {response.status_code} - {response.text}")
        except Exception as e:
            _logger.error(f"Weather Fetch Exception: {str(e)}")
