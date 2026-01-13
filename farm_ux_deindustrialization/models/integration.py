from odoo import models, api, fields
import json
import logging

_logger = logging.getLogger(__name__)


class IrUiView(models.Model):
    _inherit = 'ir.ui.view'

    def get_view(self, view_id=None, view_type='form', **options):
        """统一处理视图定制：术语映射 + 布局模板"""
        result = super().get_view(view_id=view_id, view_type=view_type, **options)

        # 1. 应用术语映射
        arch = result.get('arch')
        if arch:
            # 调用 term.mapping 逻辑
            result['arch'] = self.env['term.mapping'].apply_term_mapping_to_text(arch)

        # 2. 应用表单布局模板
        if view_type in ['form', 'tree', 'kanban']:
            try:
                model_name = result.get('model')
                if model_name:
                    template = self.env['form.layout.template'].search([
                        ('model_name', '=', model_name),
                        ('is_active', '=', True)
                    ], limit=1)

                    if template and template.layout_definition:
                        # 预留给未来复杂的布局干预逻辑
                        pass
            except Exception as e:
                _logger.error("Error applying layout templates: %s", e)

        return result


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        """将无障碍配置和 UX 定制注入 session_info，提升前端加载速度"""
        result = super().session_info()
        if self.env.user:
            try:
                # 注入无障碍功能
                result['accessibility_features'] = self.env['accessibility.settings'].get_user_accessibility_features(self.env.user.id)
                # 注入工作空间定制
                result['workspace_customization'] = self.env['workspace.customization'].get_user_customization(self.env.user.id)
            except Exception as e:
                _logger.error("Error adding UX features to session_info: %s", e)
        return result


class AccessibilityIntegration(models.AbstractModel):
    """前端组件需要的 RPC 接口 [US-16-09]"""
    _name = 'accessibility.integration'
    _description = 'Accessibility Integration RPC'

    @api.model
    def get_accessibility_features(self, user_id=None):
        return self.env['accessibility.settings'].get_user_accessibility_features(user_id or self.env.uid)

    @api.model
    def get_contextual_help_data(self, model_name, view_type='form', field_name=None):
        """获取当前上下文的帮助数据"""
        help_records = self.env['contextual.help'].get_contextual_help(model_name, field_name, view_type)
        return [{
            'id': r.id,
            'name': r.name,
            'content': r.help_content,
            'video_url': r.help_video_url,
            'level': r.difficulty_level,
        } for r in help_records]


class AccessibilitySettings(models.Model):
    _inherit = 'accessibility.settings'

    @api.model
    def get_user_accessibility_features(self, user_id):
        """获取用户的无障碍功能配置"""
        settings = self.search([('user_id', '=', user_id)], limit=1)
        if settings:
            return {
                'screen_reader_enabled': settings.screen_reader_enabled,
                'keyboard_navigation': settings.keyboard_navigation,
                'font_scaling': settings.font_scaling,
                'high_contrast_mode': settings.high_contrast_mode,
                'large_touch_targets': settings.large_touch_targets,
                'reduced_motion': settings.reduced_motion,
                'color_blind_mode': settings.color_blind_mode,
                'voice_navigation': settings.voice_navigation,
            }
        return {}


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    def message_post(self, **kwargs):
        """重写 message_post 方法以支持社交网络"""
        result = super(MailThread, self).message_post(**kwargs)
        
        # 检查是否需要将消息发布到社交网络
        if hasattr(self, '_need_post_to_social_network') and self._need_post_to_social_network():
            try:
                self.env['farm.social.network.integration'].post_message_to_network(self, result)
            except Exception as e:
                _logger.error(f"Error posting to social network: {e}")
        
        return result


class FarmSocialNetworkIntegration(models.AbstractModel):
    _name = 'farm.social.network.integration'
    _description = 'Farm Social Network Integration'

    @api.model
    def post_message_to_network(self, record, message):
        """实现具体的发布逻辑"""
        pass