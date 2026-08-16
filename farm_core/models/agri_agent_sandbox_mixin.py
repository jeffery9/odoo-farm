# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import json

class AgriAgentSandboxMixin(models.AbstractModel):
    _name = 'agri.agent.sandbox.mixin'
    _description = 'AI Agent Tool Sandbox Mixin'

    def action_invoke_agent_tool(self, agent_id, action_name, payload_data, risk_tier):
        """ Intercept agent tool invocation and route according to 3-tier security gateway """
        if risk_tier == 'green':
            return self._execute_sandbox_action(action_name, payload_data)
            
        elif risk_tier == 'yellow':
            res = self._execute_sandbox_action(action_name, payload_data)
            # Log audit trail to a unified executed tool request
            request = self.env['agri.agent.tool.request'].create({
                'agent_identifier': agent_id,
                'target_action': action_name,
                'payload': json.dumps(payload_data),
                'risk_tier': 'yellow',
                'state': 'executed'
            })
            request.message_post(body=_("Yellow-Tier GxP Tool Auto-Executed by agent '%s'. Action: %s. Payload: %s") % (
                agent_id, action_name, json.dumps(payload_data)
            ))
            return res
            
        elif risk_tier == 'red':
            # Create a pending GxP tool request using a separate cursor to persist across rollbacks
            new_cr = self.env.registry.cursor()
            try:
                new_env = self.env(cr=new_cr)
                request = new_env['agri.agent.tool.request'].create({
                    'agent_identifier': agent_id,
                    'target_action': action_name,
                    'payload': json.dumps(payload_data),
                    'risk_tier': 'red',
                    'state': 'pending'
                })
                req_name = request.name
                new_cr.commit()
            finally:
                new_cr.close()

            # Suspend transaction and raise bilingual Validation Error
            raise ValidationError(
                f"GXP_RED_TIER_APPROVAL_REQUIRED: Red-tier physical action '{action_name}' was blocked and suspended. "
                f"A GxP human-in-the-loop approval request has been generated as {req_name}. "
                f"(红级关键操作'{action_name}'已被拦截挂起。人类审核单 {req_name} 已生成，待手动批准后方可执行。)"
            )

    def _execute_sandbox_action(self, action_name, payload_data):
        """ Execute local action dynamically """
        if hasattr(self, action_name):
            method = getattr(self, action_name)
            if action_name == 'write':
                return method(payload_data)
            return method(**payload_data)
        raise ValidationError(_("Action %s not found on model %s") % (action_name, self._name))
