# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

class DividendDistribution(models.Model):
    _name = 'dividend.distribution'
    _description = 'Dividend Distribution Engine (JA Patronage Model)'

    name = fields.Char(string='Distribution Title', required=True)
    cooperative_id = fields.Many2one('res.company', string='Cooperative (Company)', required=True, default=lambda self: self.env.company)
    total_profit = fields.Float(string='Total Profit to Distribute', required=True)
    
    # 50% shares, 50% patronage (Trading Volume)
    share_weight = fields.Float(string='Share-Based Weight (%)', default=50.0, required=True)
    patronage_weight = fields.Float(string='Patronage Weight (%)', default=50.0, required=True)
    
    line_ids = fields.One2many('dividend.line', 'distribution_id', string='Dividend Lines')
    state = fields.Selection([('draft', 'Draft'), ('calculated', 'Calculated'), ('executed', 'Executed')], default='draft')

    def action_calculate(self):
        self.line_ids.unlink()
        members = self.env['farm.entity'].search([('company_id', '=', self.cooperative_id.id), ('entity_type', 'in', ['smallholder', 'family_farm'])])
        
        total_shares = sum(m.share_ratio for m in members)
        # Simplified: We mock total trading volume for the demo
        total_volume = sum(m.trading_volume for m in members) if hasattr(members, 'trading_volume') else 100000.0

        lines = []
        for member in members:
            # 1. Share-based Dividend
            share_portion = 0.0
            if total_shares > 0:
                share_portion = (self.total_profit * (self.share_weight / 100.0)) * (member.share_ratio / total_shares)
            
            # 2. Patronage (Volume-based) Dividend (The JA Model)
            patronage_portion = 0.0
            member_volume = member.trading_volume if hasattr(member, 'trading_volume') else 1000.0
            if total_volume > 0:
                patronage_portion = (self.total_profit * (self.patronage_weight / 100.0)) * (member_volume / total_volume)
                
            total_dividend = share_portion + patronage_portion
            
            if total_dividend > 0:
                lines.append((0, 0, {
                    'member_id': member.id,
                    'share_amount': share_portion,
                    'patronage_amount': patronage_portion,
                    'total_amount': total_dividend,
                }))
        
        self.write({'line_ids': lines, 'state': 'calculated'})

    def action_execute(self):
        for line in self.line_ids:
            self.env['internal.settlement'].create({
                'from_entity_id': self.cooperative_id.partner_id.id,
                'to_entity_id': line.member_id.partner_id.id,
                'amount': line.total_amount,
                'type': 'dividend',
                'state': 'done'
            })
        self.state = 'executed'


class DividendLine(models.Model):
    _name = 'dividend.line'
    _description = 'Dividend Line (Supports Patronage)'

    distribution_id = fields.Many2one('dividend.distribution', ondelete='cascade')
    member_id = fields.Many2one('farm.entity', string='Member')
    share_amount = fields.Float(string='Share-Based Dividend')
    patronage_amount = fields.Float(string='Patronage (Volume-Based) Dividend')
    total_amount = fields.Float(string='Total Dividend')
