import re

with open('farm_ai_agent/models/mission_orchestrator.py', 'r') as f:
    content = f.read()

# Strip mission_id field
content = re.sub(r'    mission_id = fields\.Many2one\(\'farm\.robot\.mission\', string="Dispatched Mission"\)\n', '', content)

# Strip the content of _dispatch_remediation_mission
# Basically keep:
# def _dispatch_remediation_mission(self, twin):
#     # Logic handled by bridge
#     pass
import re
new_method = """    def _dispatch_remediation_mission(self, twin):
        # Implementation delegated to farm_ai_robotics_bridge
        pass"""
content = re.sub(r'    def _dispatch_remediation_mission\(self, twin\):.*?(?=\n\nclass AIAutonomousMissionLog)', new_method, content, flags=re.DOTALL)

with open('farm_ai_agent/models/mission_orchestrator.py', 'w') as f:
    f.write(content)

with open('farm_ai_agent/models/a2a_negotiation.py', 'r') as f:
    content = f.read()

# Original _evaluate_proposal_logic in a2a_negotiation.py
# 2. Delegate to specialized agents (e.g. Robots)
# if self.receiver_agent_id.startswith('robot:'):
#     robot = self.env['farm.robot'].search([('agent_id', '=', self.receiver_agent_id)], limit=1)
#     if robot:
#         return robot.evaluate_a2a_proposal(incoming_payload)
# We need to replace this block.

new_method_2 = """    def _evaluate_proposal_logic(self, incoming_payload):
        # 1. Check strict parameters
        if incoming_payload.get('sustainability_score', 100) < 50:
            return {'decision': 'reject', 'reason': 'Sustainability redline exceeded'}

        # 2. Delegate to specialized agents (handled by bridge)
        
        # 3. Standard Bargaining Heuristics
        offered = incoming_payload.get('proposed_credits', 0.0)
        if offered < self.proposed_credits * 0.9:
            return {'decision': 'counter', 'counter_offer': self.proposed_credits * 0.95}
        
        return {'decision': 'accept'}"""

content = re.sub(r'    def _evaluate_proposal_logic\(self, incoming_payload\):.*?(?=\n\n    def execute_a2a_contract)', new_method_2, content, flags=re.DOTALL)

with open('farm_ai_agent/models/a2a_negotiation.py', 'w') as f:
    f.write(content)
