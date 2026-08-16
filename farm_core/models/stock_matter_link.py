# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class StockMatterTrackingLink(models.Model):
    _inherit = 'stock.matter.tracking.link'

    link_type = fields.Selection([
        ('sequential', 'Sequential (顺序流转)'),
        ('split', 'Split (拆分流转)'),
        ('fission', 'Fission (分裂流转)'),
        ('blending', 'Blending (混合流转)'),
    ], string='Link Type (链接类型)', required=True, default='sequential')

    _sql_constraints = [
        ('parent_child_unique_inherit', 'unique(parent_id, child_id)', 'Link between parent and child must be unique! (父子载体链接必须唯一！)')
    ]

    @api.model_create_multi
    def create(self, vals_list):
        records = super(StockMatterTrackingLink, self).create(vals_list)
        for record in records:
            record._check_cyclic_loop()
            record._propagate_dna_and_entropy()
        return records

    def _check_cyclic_loop(self):
        """ Check for cyclic loops using a set-based DFS path validation to avoid recursion limits """
        visited = set()
        stack = [self.child_id.id]
        while stack:
            current_id = stack.pop()
            if current_id == self.parent_id.id:
                raise ValidationError(_("Circular Dependency Detected! You cannot link a child to an upstream parent. (检测到循环依赖！无法将子级链接到上游父级。)"))
            if current_id not in visited:
                visited.add(current_id)
                links = self.search([('parent_id', '=', current_id)])
                for l in links:
                    stack.append(l.child_id.id)

    def _propagate_dna_and_entropy(self):
        """ Compute downstream DNA score with decay and penalties """
        parent = self.parent_id
        child = self.child_id
        
        # Collect all parent link scores
        incoming_links = self.search([('child_id', '=', child.id)])
        parents = incoming_links.mapped('parent_id')
        
        if len(parents) == 1:
            # Single-source: 1% entropy penalty
            decayed_dna = parents[0].dna_integrity_score * 0.99
        else:
            # Blending multi-source: average parent score minus 5% entropy penalty
            avg_score = sum(parents.mapped('dna_integrity_score')) / len(parents)
            decayed_dna = avg_score * 0.95
            
        child.write({'dna_integrity_score': max(0.0, min(100.0, decayed_dna))})
