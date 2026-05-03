# -*- coding: utf-8 -*-
# [US-16-26] [LOSSLESS] Agricultural Menu & Action Interceptor
from odoo import models, fields, api, _

class IrUiMenu(models.Model):
    _name = 'ir.ui.menu'
    _inherit = 'ir.ui.menu'

    def read(self, fields=None, load='_classic_read'):
        """ 拦截菜单读取，实时替换名称 """
        res = super(IrUiMenu, self).read(fields=fields, load=load)
        if not self.env.context.get('skip_agri_mapping'):
            TermMapping = self.env['term.mapping']
            for menu in res:
                if 'name' in menu:
                    menu['name'] = TermMapping.apply_term_mapping_to_text(menu['name'])
        return res

class IrActionsActWindow(models.Model):
    _name = 'ir.actions.act_window'
    _inherit = 'ir.actions.act_window'

    def read(self, fields=None, load='_classic_read'):
        """ 拦截动作读取，实时替换标题 """
        res = super(IrActionsActWindow, self).read(fields=fields, load=load)
        if not self.env.context.get('skip_agri_mapping'):
            TermMapping = self.env['term.mapping']
            for action in res:
                if 'name' in action:
                    action['name'] = TermMapping.apply_term_mapping_to_text(action['name'])
                if 'help' in action and isinstance(action['help'], str):
                    action['help'] = TermMapping.apply_term_mapping_to_text(action['help'])
        return res