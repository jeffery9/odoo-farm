from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class BaseSequenceMixin(models.AbstractModel):
    """
    混合类：提供标准的序列号生成功能
    """
    _name = 'base.sequence.mixin'
    _description = 'Base Sequence Mixin'

    @api.model
    def create(self, vals):
        """通用的创建方法，使用序列号生成name字段"""
        if vals.get('name', _('New')) == _('New'):
            sequence_code = self._name.replace('.', '_')
            vals['name'] = self.env['ir.sequence'].next_by_code(sequence_code) or '/'
        return super().create(vals)


class BaseCodeMixin(models.AbstractModel):
    """
    混合类：提供标准的代码字段生成功能
    """
    _name = 'base.code.mixin'
    _description = 'Base Code Mixin'

    @api.model
    def create(self, vals):
        """通用的创建方法，使用序列号生成code字段"""
        if 'code' not in vals or not vals['code']:
            sequence_code = self._name.replace('.', '_')
            vals['code'] = self.env['ir.sequence'].next_by_code(sequence_code) or '/'
        return super().create(vals)


class BaseTotalAmountMixin(models.AbstractModel):
    """
    混合类：提供标准的总额计算功能
    """
    _name = 'base.total.amount.mixin'
    _description = 'Base Total Amount Mixin'

    @api.depends('quantity', 'unit_price')
    def _compute_total_amount(self):
        """通用的总额计算方法"""
        for record in self:
            record.total_amount = record.quantity * record.unit_price


class BaseInvestmentAmountMixin(models.AbstractModel):
    """
    混合类：提供投资相关金额计算功能
    """
    _name = 'base.investment.amount.mixin'
    _description = 'Base Investment Amount Mixin'

    @api.depends('shares_count', 'share_price')
    def _compute_total_amount(self):
        """股份交易总额计算"""
        for record in self:
            record.total_amount = record.shares_count * record.share_price


class BaseServiceAmountMixin(models.AbstractModel):
    """
    混合类：提供服务相关金额计算功能
    """
    _name = 'base.service.amount.mixin'
    _description = 'Base Service Amount Mixin'

    @api.depends('service_quantity', 'unit_rate')
    def _compute_total_amount(self):
        """服务订单总额计算"""
        for record in self:
            record.total_amount = record.service_quantity * record.unit_rate


class BaseActionConfirmMixin(models.AbstractModel):
    """
    混合类：提供标准的确认操作功能
    """
    _name = 'base.action.confirm.mixin'
    _description = 'Base Action Confirm Mixin'

    def action_confirm(self):
        """通用的确认操作方法"""
        for record in self:
            if record.state == 'draft':
                record.state = 'confirmed'


class BaseActionApproveMixin(models.AbstractModel):
    """
    混合类：提供标准的批准操作功能
    """
    _name = 'base.action.approve.mixin'
    _description = 'Base Action Approve Mixin'

    def action_approve(self):
        """通用的批准操作方法"""
        for record in self:
            record.state = 'approved'


class BaseActionRejectMixin(models.AbstractModel):
    """
    混合类：提供标准的拒绝操作功能
    """
    _name = 'base.action.reject.mixin'
    _description = 'Base Action Reject Mixin'

    def action_reject(self):
        """通用的拒绝操作方法"""
        for record in self:
            record.state = 'rejected'


class BaseActionCancelMixin(models.AbstractModel):
    """
    混合类：提供标准的取消操作功能
    """
    _name = 'base.action.cancel.mixin'
    _description = 'Base Action Cancel Mixin'

    def action_cancel(self):
        """通用的取消操作方法"""
        for record in self:
            if record.state in ['draft', 'confirmed']:
                record.state = 'cancelled'


class BaseCreditLimitMixin(models.AbstractModel):
    """
    混合类：提供信用额度验证功能
    """
    _name = 'base.credit.limit.mixin'
    _description = 'Base Credit Limit Mixin'

    @api.constrains('credit_limit', 'utilized_amount')
    def _check_credit_limit(self):
        """验证信用额度限制"""
        for record in self:
            if record.utilized_amount > record.credit_limit:
                raise ValidationError(_('Utilized amount cannot exceed credit limit.'))


class BaseLoanAmountMixin(models.AbstractModel):
    """
    混合类：提供贷款金额验证功能
    """
    _name = 'base.loan.amount.mixin'
    _description = 'Base Loan Amount Mixin'

    @api.constrains('loan_amount')
    def _check_loan_amount(self):
        """验证贷款金额"""
        for record in self:
            if record.loan_amount <= 0:
                raise ValidationError(_('Loan amount must be positive.'))


class BaseAvailableAmountMixin(models.AbstractModel):
    """
    混合类：提供可用金额计算功能
    """
    _name = 'base.available.amount.mixin'
    _description = 'Base Available Amount Mixin'

    @api.depends('credit_limit', 'utilized_amount')
    def _compute_available_amount(self):
        """计算可用金额"""
        for record in self:
            record.available_amount = record.credit_limit - record.utilized_amount


class BaseShareValueMixin(models.AbstractModel):
    """
    混合类：提供股份价值计算功能
    """
    _name = 'base.share.value.mixin'
    _description = 'Base Share Value Mixin'

    @api.depends('shares_held')
    def _compute_share_value(self):
        """计算股份价值"""
        for record in self:
            # Simple calculation - in real implementation this might be based on share price
            record.share_value = record.shares_held * 100.0  # Assuming 100 per share


class BaseTotalInvestmentMixin(models.AbstractModel):
    """
    混合类：提供总投资计算功能
    """
    _name = 'base.total.investment.mixin'
    _description = 'Base Total Investment Mixin'

    @api.depends('share_value')
    def _compute_total_investment(self):
        """计算总投资"""
        for record in self:
            # May include other investment types in the future
            record.total_investment = record.share_value


class BaseAvailableCreditMixin(models.AbstractModel):
    """
    混合类：提供可用信用计算功能
    """
    _name = 'base.available.credit.mixin'
    _description = 'Base Available Credit Mixin'

    @api.depends('credit_limit', 'credit_used')
    def _compute_available_credit(self):
        """计算可用信用"""
        for record in self:
            record.available_credit = record.credit_limit - record.credit_used


class BaseComplianceStatusMixin(models.AbstractModel):
    """
    混合类：提供合规状态计算功能
    """
    _name = 'base.compliance.status.mixin'
    _description = 'Base Compliance Status Mixin'

    @api.depends('audit_result')
    def _compute_compliance(self):
        """计算合规状态"""
        for record in self:
            record.compliance_status = (record.audit_result == 'authorized')


class BaseCertifiedStatusMixin(models.AbstractModel):
    """
    混合类：提供认证状态计算功能
    """
    _name = 'base.certified.status.mixin'
    _description = 'Base Certified Status Mixin'

    @api.depends('quality_score', 'standard_id', 'expiry_date', 'state')
    def _compute_certified_status(self):
        """计算认证状态"""
        for record in self:
            if (record.state == 'approved' and
                record.quality_score and
                record.standard_id and
                record.quality_score >= record.standard_id.quality_threshold and
                (not record.expiry_date or record.expiry_date >= fields.Date.context_today(self))):
                record.is_certified = True
            else:
                record.is_certified = False


class BaseNetAmountMixin(models.AbstractModel):
    """
    混合类：提供净额计算功能
    """
    _name = 'base.net.amount.mixin'
    _description = 'Base Net Amount Mixin'

    @api.depends('receivable_amount', 'payable_amount')
    def _compute_net_amount(self):
        """计算净额"""
        for record in self:
            record.net_amount = record.receivable_amount - record.payable_amount


class BaseSettlementDirectionMixin(models.AbstractModel):
    """
    混合类：提供结算方向计算功能
    """
    _name = 'base.settlement.direction.mixin'
    _description = 'Base Settlement Direction Mixin'

    @api.depends('net_amount')
    def _compute_settlement_direction(self):
        """计算结算方向"""
        for record in self:
            if record.net_amount > 0:
                record.settlement_direction = 'to_member'
            elif record.net_amount < 0:
                record.settlement_direction = 'from_member'
            else:
                record.settlement_direction = False


class BaseAmountCalculationMixin(models.AbstractModel):
    """
    混合类：提供金额计算功能
    """
    _name = 'base.amount.calculation.mixin'
    _description = 'Base Amount Calculation Mixin'

    @api.depends('quantity', 'unit_price')
    def _compute_member_amount(self):
        """计算成员金额"""
        for line in self:
            line.member_amount = line.quantity * line.unit_price

    @api.depends('member_amount')
    def _compute_markup_amount(self):
        """计算加价金额"""
        for line in self:
            if line.procurement_id:
                markup_rate = line.procurement_id.markup_rate / 100.0
                line.markup_amount = line.member_amount * markup_rate