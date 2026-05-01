import os
import re

def convert_constraints(content):
    # Regex to capture the entire _sql_constraints array block
    # It looks for _sql_constraints... = [ ... ]
    # It handles both commented and uncommented variants
    pattern = r"((?:#\s*)?(?:_sql_constraints|_sql_constraints_backup)\s*=\s*\[(.*?)\])"
    
    def replacer(match):
        full_match = match.group(1)
        inner_content = match.group(2)
        
        # Clean up the inner content (remove leading '#' and extra whitespace)
        lines = inner_content.split('\n')
        clean_lines = []
        for line in lines:
            line = re.sub(r"^\s*#\s*", "", line)
            if line.strip():
                clean_lines.append(line)
        
        clean_content = "\n".join(clean_lines)
        
        # Now find individual tuples: ('name', 'definition', 'message')
        tuple_pattern = r"\(\s*['\"](.*?)['\"]\s*,\s*['\"](.*?)['\"]\s*,\s*['\"](.*?)['\"]\s*\)"
        
        constraints = []
        for tup_match in re.finditer(tuple_pattern, clean_content, re.DOTALL):
            name = tup_match.group(1).replace('.', '_').replace('-', '_')
            definition = tup_match.group(2).replace("'", "\\'")
            message = tup_match.group(3).replace("'", "\\'")
            
            # Format to Odoo 19 models.Constraint
            # Prepend an underscore to the name to make it a protected class attribute
            c_str = f"    _{name} = models.Constraint(\n        '{definition}',\n        '{message}'\n    )"
            constraints.append(c_str)
        
        if constraints:
            return "\n".join(constraints)
        return full_match # return original if parsing failed

    new_content = re.sub(pattern, replacer, content, flags=re.DOTALL)
    return new_content

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = convert_constraints(content)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Migrated constraints in: {filepath}")

for root, dirs, files in os.walk('.'):
    if '.git' in root or '.pytest_cache' in root:
        continue
    for file in files:
        if file.endswith('.py'):
            process_file(os.path.join(root, file))
