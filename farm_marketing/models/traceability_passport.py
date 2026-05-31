from odoo import models, fields, api, _
import json

class StockLotPassport(models.Model):
    _inherit = 'stock.lot'

    traceability_passport_json = fields.Text("Traceability Passport Data", compute="_compute_passport_data")

    @api.model
    def _get_passport_plugins(self):
        """
        Registry for Traceability Passport plugins.
        Different modules should override this to add their own sections.
        """
        return [
            {'name': 'core', 'class': 'agri.passport.plugin.core'},
            {'name': 'carbon', 'class': 'agri.passport.plugin.carbon'},
            {'name': 'gs1', 'class': 'agri.passport.plugin.gs1'},
        ]

    def _compute_passport_data(self):
        """
        [US-MKT-01] [SOLID Refactored]
        Generates a rich JSON payload for consumer-facing QR Codes via plugins.
        """
        for lot in self:
            passport_data = {
                "lot_number": lot.name,
                "product": lot.product_id.name,
                "marketing_story": lot.product_id.description_sale or "Farm fresh product.",
                "sections": []
            }

            plugins = self._get_passport_plugins()
            for plugin_info in plugins:
                plugin_model = self.env.get(plugin_info['class'])
                if plugin_model:
                    try:
                        section = plugin_model.generate_section(lot)
                        if section:
                            passport_data['sections'].append(section)
                    except Exception as e:
                        _logger.error(f"Passport Plugin Error ({plugin_info['name']}): {str(e)}")

            lot.traceability_passport_json = json.dumps(passport_data, indent=2)


class AgriPassportPlugin(models.AbstractModel):
    """
    Interface for Traceability Passport Plugins.
    """
    _name = 'agri.passport.plugin'
    _description = 'Traceability Passport Plugin Interface'

    @api.model
    def generate_section(self, lot):
        """
        Returns a dictionary representing a section in the passport.
        Example: {'title': 'Field History', 'data': [...]}
        """
        return {}


class AgriPassportPluginCore(models.AbstractModel):
    """ [Plugin] Core Intervention & Harvest Metadata """
    _name = 'agri.passport.plugin.core'
    _inherit = 'agri.passport.plugin'

    @api.model
    def generate_section(self, lot):
        data = {
            'title': _('Farm Operations'),
            'icon': 'fa-calendar',
            'metrics': []
        }
        
        interventions = self.env['mrp.production'].search([('lot_producing_id', '=', lot.id)])
        data['metrics'].append({'label': _('Total Interventions'), 'value': len(interventions)})
        
        harvest = interventions.filtered(lambda i: i.intervention_type == 'harvesting')
        if harvest and harvest[0].date_finished:
            data['metrics'].append({'label': _('Harvest Date'), 'value': harvest[0].date_finished.strftime('%Y-%m-%d')})
            
        drones = interventions.filtered(lambda i: i.intervention_type == 'aerial_spraying')
        data['metrics'].append({'label': _('Smart Drone Flights'), 'value': len(drones)})
        
        return data


class AgriPassportPluginCarbon(models.AbstractModel):
    """ [Plugin] ESG Carbon Footprint Metrics """
    _name = 'agri.passport.plugin.carbon'
    _inherit = 'agri.passport.plugin'

    @api.model
    def generate_section(self, lot):
        if 'agri.carbon.ledger' not in self.env:
            return {}
            
        ledgers = self.env['agri.carbon.ledger'].search([('lot_id', '=', lot.id)])
        total_co2 = 0.0
        for ledger in ledgers:
            if ledger.impact_type == 'sequestration':
                total_co2 -= ledger.co2e_amount
            else:
                total_co2 += ledger.co2e_amount
        
        return {
            'title': _('Sustainability DNA'),
            'icon': 'fa-leaf',
            'metrics': [
                {'label': _('Net Carbon Footprint (kg CO2e)'), 'value': round(total_co2, 2)}
            ]
        }


class AgriPassportPluginGS1(models.AbstractModel):
    """ [Plugin] GS1 EPCIS Digital Link & Identity """
    _name = 'agri.passport.plugin.gs1'
    _inherit = 'agri.passport.plugin'

    @api.model
    def generate_section(self, lot):
        # Build standard GS1 identifiers
        gtin = getattr(lot.product_id, 'gs1_gtin', False) or "00000000000000"
        lot_sn = lot.name
        
        # EPCIS URI Format (Simplified)
        epc_uri = f"urn:epc:class:lgtin:{gtin}.{lot_sn}"
        
        data = {
            'title': _('Global Interoperability'),
            'icon': 'fa-globe',
            'metrics': [
                {'label': 'GS1 GTIN', 'value': gtin},
                {'label': 'EPC URI', 'value': epc_uri},
            ],
            'epcis_json_ld': self._generate_epcis_snippet(lot, epc_uri)
        }
        
        return data

    def _generate_epcis_snippet(self, lot, epc_uri):
        """ Generates a valid GS1 EPCIS 2.0 JSON-LD snippet """
        snippet = {
            "@context": "https://ref.gs1.org/standards/epcis/2.0.0/epcis-context.jsonld",
            "type": "TransformationEvent",
            "eventTime": fields.Datetime.now().isoformat(),
            "eventTimeZoneOffset": "+00:00",
            "epcList": [epc_uri],
            "bizStep": "harvesting", # Default
            "readPoint": {"id": f"urn:epc:id:sgln:{lot.company_id.gs1_gln or '0000000000000'}.0"}
        }
        return snippet

