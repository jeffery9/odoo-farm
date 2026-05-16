from odoo import models, fields, api, _
from odoo.exceptions import UserError

class FarmNurseryBatch(models.Model):
    _inherit = 'farm.nursery.batch'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('parent_p1_id') and vals.get('parent_p2_id'):
                sire = self.env['stock.lot'].browse(vals['parent_p1_id'])
                dam = self.env['stock.lot'].browse(vals['parent_p2_id'])
                
                # 1. Inbreeding Check
                sire_ancestors = sire.get_ancestors(depth=3)
                dam_ancestors = dam.get_ancestors(depth=3)
                if sire_ancestors.intersection(dam_ancestors):
                    raise UserError(_("Inbreeding Risk: Sire and Dam share common ancestors within 3 generations."))
                
                # 2. Lethal Gene Collision Check
                if sire.dna_marker and dam.dna_marker and 'LETHAL' in sire.dna_marker and sire.dna_marker == dam.dna_marker:
                    raise UserError(_("Lethal Gene Collision: Both parents carry the recessive lethal marker %s.") % sire.dna_marker)

        # Proceed with creation
        records = super().create(vals_list)
        
        # 3. Trait Inheritance
        for record in records:
            if record.parent_p1_id and record.parent_p2_id:
                sire = record.parent_p1_id
                dam = record.parent_p2_id
                
                # Gather traits
                sire_traits = {t.name: t.score for t in sire.trait_value_ids}
                dam_traits = {t.name: t.score for t in dam.trait_value_ids}
                
                all_trait_names = set(sire_traits.keys()).union(dam_traits.keys())
                
                inherited_traits = []
                for t_name in all_trait_names:
                    s_score = sire_traits.get(t_name, 0)
                    d_score = dam_traits.get(t_name, 0)
                    
                    # If both parents have it, average it. If one has it, halve it (simplified genetics)
                    avg_score = (s_score + d_score) / 2.0
                    
                    inherited_traits.append((0, 0, {
                        'name': t_name,
                        'score': avg_score
                    }))
                
                if inherited_traits:
                    record.lot_id.write({'trait_value_ids': inherited_traits})
                    
        return records
