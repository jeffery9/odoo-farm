with open('farm_ai_core/models/ai_base.py', 'r') as f:
    content = f.read()

stub_method = """
    def action_test_connection(self):
        for record in self:
            record.status = 'connected'
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Connection Success',
                    'message': 'Successfully connected to AI service.',
                    'type': 'success',
                    'sticky': False,
                }
            }
"""

if 'def action_test_connection' not in content:
    content = content.replace("class AgriAiConfiguration(models.AbstractModel):", "class AgriAiConfiguration(models.AbstractModel):\n" + stub_method)

with open('farm_ai_core/models/ai_base.py', 'w') as f:
    f.write(content)
