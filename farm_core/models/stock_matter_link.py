# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import hashlib

class StockMatterTrackingLink(models.Model):
    _inherit = 'stock.matter.tracking.link'

    link_type = fields.Selection([
        ('sequential', 'Sequential (顺序流转)'),
        ('split', 'Split (拆分流转)'),
        ('fission', 'Fission (分裂流转)'),
        ('blending', 'Blending (混合流转)'),
    ], string='Link Type (链接类型)', required=True, default='sequential')

    _parent_child_unique_inherit = models.Constraint(
        'unique(parent_id, child_id)',
        'Link between parent and child must be unique! (父子载体链接必须唯一！)'
    )

    @api.model_create_multi
    def create(self, vals_list):
        records = super(StockMatterTrackingLink, self).create(vals_list)
        for record in records:
            record._check_cyclic_loop()
            record._propagate_dna_and_entropy()
            
            # Decoupled Merkle recalculation queue based on config.get('test_enable')
            from odoo.tools import config
            if (config.get('test_enable') or self.env.context.get('sync_merkle')) and not self.env.context.get('force_decoupled_merkle'):
                record._calculate_and_propagate_merkle_hash()
            else:
                record._mark_pending_merkle_recalc()
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
            # Single-source: 1% entropy penalty, unless it is a split transition (5% penalty)
            decay_rate = 0.95 if self.transition_type == 'split' else 0.99
            decayed_dna = parents[0].dna_integrity_score * decay_rate
        else:
            # Blending multi-source: average parent score minus 5% entropy penalty
            avg_score = sum(parents.mapped('dna_integrity_score')) / len(parents)
            decayed_dna = avg_score * 0.95
            
        child.write({'dna_integrity_score': max(0.0, min(100.0, decayed_dna))})

    def _calculate_and_propagate_merkle_hash(self):
        """ Dynamic Merkle SHA-256 state cascade hash computation & automated ledger log """
        child = self.child_id
        incoming_links = self.search([('child_id', '=', child.id)])
        parents = incoming_links.mapped('parent_id').sorted(key=lambda r: r.id)
        
        # Assemble parent hash blocks
        parent_hashes = [p.merkle_state_hash or p.name for p in parents]
        parent_block = ",".join(parent_hashes)
        
        # Child metadata block
        child_block = f"{child.name}:{child.dna_integrity_score}"
        
        # Combined SHA-256 cascade
        combined_payload = f"[{parent_block}]->[{child_block}]"
        merkle_hash = hashlib.sha256(combined_payload.encode('utf-8')).hexdigest()
        
        child.write({'merkle_state_hash': merkle_hash})
        
        # Automated certified ledger audit log
        self.env['agri.clearing.ledger'].create({
            'partner_id': self.env.user.partner_id.id,
            'credit_change': 0.0,
            'score_change': 1,
            'description': f"SFC Merkle Traceability State Certified: Hash={merkle_hash[:16]} (SFC 级联 Merkle 密码学状态验证成功)",
            'state': 'confirmed'
        })

    def _mark_pending_merkle_recalc(self):
        """ Mark child and all its downstream descendants as pending Merkle recalculation """
        queue = [self.child_id.id]
        visited = set()
        while queue:
            current_id = queue.pop(0)
            if current_id in visited:
                continue
            visited.add(current_id)
            self.env['stock.matter.tracking'].browse(current_id).write({
                'pending_merkle_recalc': True
            })
            links = self.search([('parent_id', '=', current_id)])
            for link in links:
                queue.append(link.child_id.id)
