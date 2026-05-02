import re
with open('farm_operation/models/project_task.py', 'r') as f:
    content = f.read()

content = re.sub(r"    @api\.constrains\('user_ids', '# required_skill_ids', '# required_certification_ids'\)\n    def _check_employee_qualifications\(self\):\n        pass\n", "", content)

with open('farm_operation/models/project_task.py', 'w') as f:
    f.write(content)
