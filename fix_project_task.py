with open('farm_operation/models/project_task.py', 'r') as f:
    lines = f.readlines()

with open('farm_operation/models/project_task.py', 'w') as f:
    for line in lines:
        if "# required_skill_ids = fields.Many2many(" in line or "'farm.training.skill'," in line or "string=\"Required Skills\"," in line or "help=\"Skills required to perform this task.\"" in line or "#     )" in line:
            continue
        if "# required_certification_ids = fields.Many2many(" in line or "'farm.training.certification'," in line or "string=\"Required Certifications\"," in line or "help=\"Certifications required to perform this task.\"" in line:
            continue
        # Also clean up the remaining un-commented parts
        if "    # required_certification_ids = fields.Many2many(" in line:
            continue
        f.write(line)
