# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class A2AReactLoop(models.Model):
    """
    A2A Re-Act execution loop model.
    Tracks reasoning, actions, and observations in sequence.
    """
    _name = 'agri.a2a.react.loop'
    _description = 'A2A React Execution Loop'
    _inherit = ['mail.thread']

    name = fields.Char('Reference', required=True, default=lambda self: self.env['ir.sequence'].next_by_code('agri.a2a.react.loop') or 'New')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('running', 'Running'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ], default='draft', tracking=True)

    goal = fields.Text('Target Goal', required=True)
    max_iterations = fields.Integer('Max Iterations', default=10)
    current_iteration = fields.Integer('Current Iteration', default=0)
    context_data = fields.Text('JSON Context Payload', default='{}')
    skill_id = fields.Many2one('agri.ai.agent.skill', string='Loaded Skill')
    active_skill_json = fields.Text('Active Skill Directive (JSON)', default='{}')

    line_ids = fields.One2many('agri.a2a.react.loop.line', 'loop_id', string='Steps')

    @api.onchange('skill_id')
    def _onchange_skill_id(self):
        """ Pull authored/uploaded skill payload into active_skill_json """
        if self.skill_id:
            self.active_skill_json = self.skill_id.skill_payload

    def action_execute_active_skill(self, test_target_record_id=False):
        """
        Loads the active_skill_json and executes the parsed directive using a safe tool call.
        """
        self.ensure_one()
        import json
        if not self.active_skill_json or self.active_skill_json == '{}':
            return False

        try:
            payload = json.loads(self.active_skill_json)
            model_name = payload.get('model')
            method_name = payload.get('method')
            thought = payload.get('thought', 'Executing active skill directive.')
            args = payload.get('args', {})

            if not model_name or not method_name:
                raise ValueError(_("Active Skill payload must contain both 'model' and 'method' parameters."))

            # Auto-register/find safety tool in registry
            tool = self.env['agri.a2a.react.tool'].search([
                ('model_name', '=', model_name),
                ('method_name', '=', method_name),
            ], limit=1)

            if not tool:
                tool = self.env['agri.a2a.react.tool'].create({
                    'name': _("Auto Skill Tool: %s.%s") % (model_name, method_name),
                    'model_name': model_name,
                    'method_name': method_name,
                })

            # Execute via Re-Act Loop Controller under savepoint isolation
            return self.action_execute_iteration(
                thought=thought,
                action_type='tool_call',
                tool_id=tool.id,
                action_payload=json.dumps(args),
                test_target_record_id=test_target_record_id
            )
        except Exception as e:
            _logger.error("Failed to parse and execute active skill: %s", str(e))
            self.state = 'failed'
            return False

    def action_execute_iteration(self, thought, action_type, tool_id=False, action_payload='{}', test_target_record_id=False):
        """
        Executes a single Re-Act loop step safely encapsulated inside a transaction savepoint.
        """
        self.ensure_one()
        import json
        
        # Guard limits
        if self.current_iteration >= self.max_iterations:
            self.state = 'failed'
            return False

        self.current_iteration += 1
        iteration_index = self.current_iteration

        # Create unrolled iteration line record first
        line = self.env['agri.a2a.react.loop.line'].create({
            'loop_id': self.id,
            'iteration': iteration_index,
            'thought': thought,
            'action_type': action_type,
            'tool_id': tool_id,
            'action_payload': action_payload,
            'state': 'executing',
        })

        if action_type == 'terminate':
            line.write({
                'state': 'success',
                'observation': 'Loop termination requested by agent. Goal accomplished successfully.'
            })
            self.state = 'completed'
            return True

        if action_type == 'human_approve':
            line.write({
                'state': 'draft',
                'observation': 'Awaiting human verification and physical sign-off.'
            })
            self.state = 'paused'
            return True

        if action_type == 'tool_call' and tool_id:
            tool = self.env['agri.a2a.react.tool'].browse(tool_id)
            if not tool.exists() or not tool.is_active:
                line.write({
                    'state': 'failed',
                    'observation': 'ERROR: Request tool is either inactive or does not exist.'
                })
                self.state = 'failed'
                return False

            if tool.required_gxp_gating:
                # GxP/CCP gating: Pause loop and require manual sign-off
                line.write({
                    'state': 'draft',
                    'observation': 'GxP Critical Control Point triggered. Loop paused awaiting human release.'
                })
                self.state = 'paused'
                return True

            # Enter Transaction Savepoint Block
            try:
                with self.env.cr.savepoint():
                    # Parse args
                    args = json.loads(action_payload or '{}')
                    
                    # Dynamically fetch target model
                    Model = self.env[tool.model_name]
                    
                    # Resolve record ID (use test_target_record_id if provided, otherwise check context/args)
                    record_id = test_target_record_id or args.get('id') or args.get('record_id')
                    
                    if record_id:
                        record = Model.browse(int(record_id))
                        if not record.exists():
                            raise ValueError(_("Target record with ID %s not found.") % record_id)
                            
                        # Call method dynamically
                        func = getattr(record, tool.method_name)
                        # We pass the remaining arguments excluding the ID
                        call_args = {k: v for k, v in args.items() if k not in ['id', 'record_id']}
                        if tool.method_name == 'write':
                            res = func(call_args)
                        else:
                            res = func(**call_args)
                    else:
                        # Model-level static method call
                        func = getattr(Model, tool.method_name)
                        if tool.method_name == 'create':
                            res = func(args)
                        else:
                            res = func(**args)
                        
                    # If execution is successful, write observation in this transaction
                    line.write({
                        'state': 'success',
                        'observation': json.dumps({'status': 'success', 'result': str(res)})
                    })
            except Exception as e:
                # Automatically rolled back! Update logging status in separate outer transaction
                _logger.warning("Re-Act execution failed. Rolling back transaction: %s", str(e))
                line.write({
                    'state': 'violated' if 'haccp' in str(e).lower() or 'violation' in str(e).lower() or 'validation' in str(e).lower() or 'usererror' in str(e).lower() else 'failed',
                    'observation': 'ERROR/ROLLBACK: ' + str(e)
                })
                self.state = 'failed'
                return False

        return True


class A2AReadLoopLine(models.Model):
    _name = 'agri.a2a.react.loop.line'
    _description = 'A2A React Step Detail'
    _order = 'iteration'

    loop_id = fields.Many2one('agri.a2a.react.loop', string='Parent Loop', required=True, ondelete='cascade')
    iteration = fields.Integer('Iteration Sequence', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('executing', 'Executing'),
        ('success', 'Success'),
        ('violated', 'GxP Violated / Rolled Back'),
        ('failed', 'Exception Failed')
    ], default='draft')

    thought = fields.Text('Thought Processes', required=True)
    action_type = fields.Selection([
        ('tool_call', 'Odoo Tool Execution'),
        ('human_approve', 'Requires Manual Approval'),
        ('terminate', 'Finish Loop / Goal Reached')
    ], default='tool_call', required=True)

    tool_id = fields.Many2one('agri.a2a.react.tool', string='Odoo Tool')
    action_payload = fields.Text('JSON Payload', default='{}')
    observation = fields.Text('Observation Result')
