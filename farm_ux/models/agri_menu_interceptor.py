from odoo import models, fields, api, _

class AgriMenuInterceptor(models.Model):
    """
    Level 0: Deep Menu Interception.
    Dynamically hides industrial/manufacturing menus from the UI.
    """
    _inherit = 'ir.ui.menu'

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        """
        Intercepts menu searches to filter out industrial terms for 2026 de-industrialization.
        """
        industrial_keywords = [
            'Manufacturing', 'MRP', 'Work Centers', 'Bill of Materials', 
            'Work Orders', 'Master Production Schedule', 'Routing'
        ]
        
        # Add filter to exclude industrial menus by name
        new_args = list(args) if args else []
        for keyword in industrial_keywords:
            new_args.append(('name', 'not ilike', keyword))
            
        return super(AgriMenuInterceptor, self).search(
            new_args, offset=offset, limit=limit, order=order, count=count
        )
