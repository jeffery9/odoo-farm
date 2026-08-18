# -*- coding: utf-8 -*-
"""
Agri-OS L2-level Auto-Healing Engine: heal_misalignment.py
Autonomously resolves Rule 2 (Implicit Many2many relationship tables) violations across the codebase,
rewriting Python sources to use explicit relation tables, column1, and column2.
"""

import os
import ast
import re
import hashlib

base_dir = '/Users/jeffery/odoo-farm-workspace/odoo-farm-dev'

def generate_rel_names(model_name, comodel_name, field_name):
    """
    Generate postgres-safe relation table and column names under the 63-char limit.
    """
    m1 = model_name.replace('.', '_')
    m2 = comodel_name.replace('.', '_')
    
    # Base names
    rel_table = f"{m1}_{m2}_rel"
    col1 = f"{m1.split('_')[-1]}_id"
    col2 = f"{m2.split('_')[-1]}_id"
    
    # If the column names are too generic or overlap, adjust
    if col1 == col2:
        col1 = "source_id"
        col2 = "target_id"
        
    # PostgreSQL 63-char limit enforcement
    if len(rel_table) > 63:
        # Generate a unique short name using md5 hash of the original name
        h = hashlib.md5(rel_table.encode('utf-8')).hexdigest()[:8]
        # Keep prefix of model names and append hash
        rel_table = f"{m1[:20]}_{m2[:20]}_{h}_rel"
        
    # Clamp columns to 63 chars just in case
    col1 = col1[:63]
    col2 = col2[:63]
    
    return rel_table, col1, col2

def heal_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    try:
        tree = ast.parse(content, filename=file_path)
    except Exception:
        return False

    # Find the model name defined in this file (class level)
    # We map lineno of class definition to model name
    class_models = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            model_name = None
            for subnode in node.body:
                if isinstance(subnode, ast.Assign):
                    for target in subnode.targets:
                        if isinstance(target, ast.Name) and target.id in ('_name', '_inherit'):
                            if isinstance(subnode.value, ast.Constant):
                                model_name = subnode.value.value
                            elif isinstance(subnode.value, ast.Constant):
                                model_name = subnode.value.s
            if not model_name:
                # Convert CamelCase class name to snake_case as fallback
                model_name = re.sub(r'(?<!^)(?=[A-Z])', '_', node.name).lower()
            class_models[(node.lineno, node.end_lineno)] = model_name

    def get_model_for_line(lineno):
        for (start, end), m_name in class_models.items():
            if start <= lineno <= end:
                return m_name
        return "agri_generic"

    # Walk AST to find Many2many targets for healing
    m2m_nodes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and isinstance(node.value, ast.Call):
                    func = node.value.func
                    if (isinstance(func, ast.Attribute) and func.attr == 'Many2many') or \
                       (isinstance(func, ast.Name) and func.id == 'Many2many'):
                        
                        # Verify if relation table is already defined
                        has_rel_kw = any(kw.arg == 'relation' for kw in node.value.keywords)
                        if len(node.value.args) < 4 and not has_rel_kw:
                            # We found an implicit definition!
                            m2m_nodes.append((target.id, node))

    if not m2m_nodes:
        return False

    lines = content.split('\n')
    modified = False

    # Process nodes in reverse order of line number so that line indices don't shift
    m2m_nodes.sort(key=lambda x: x[1].lineno, reverse=True)

    for field_name, node in m2m_nodes:
        # Extract comodel name from first argument
        if not node.value.args:
            continue
        first_arg = node.value.args[0]
        if not isinstance(first_arg, ast.Constant) and not isinstance(first_arg, ast.Constant):
            continue
        comodel_name = first_arg.value if isinstance(first_arg, ast.Constant) else first_arg.s

        # Get the enclosing model name
        model_name = get_model_for_line(node.lineno)
        rel_table, col1, col2 = generate_rel_names(model_name, comodel_name, field_name)

        # Let's locate the line in text
        start_line = node.lineno - 1
        end_line = node.end_lineno if hasattr(node, 'end_lineno') else node.lineno
        
        # We surgically locate the Many2many call text within these lines
        m2m_text_block = "\n".join(lines[start_line:end_line])
        
        # Safe substitution regex: replace fields.Many2many('comodel' or fields.Many2many("comodel"
        pattern_str = r"fields\.Many2many\(\s*['\"]" + re.escape(comodel_name) + r"['\"]\s*"
        match = re.search(pattern_str, m2m_text_block)
        if match:
            # We insert the explicit arguments right after the comodel name
            replacement = f"fields.Many2many('{comodel_name}', '{rel_table}', '{col1}', '{col2}'"
            # If the original call has a comma after the comodel name, we append it cleanly
            original_match = match.group(0)
            
            # Check if there are other arguments
            has_comma = False
            # Look at the character right after the comodel string in original text
            idx = m2m_text_block.find(original_match) + len(original_match)
            if idx < len(m2m_text_block) and m2m_text_block[idx] in (',', ')'):
                has_comma = m2m_text_block[idx] == ','
            
            if has_comma:
                # We replace original match and the trailing comma with our replacement followed by a comma
                old_str = original_match + ','
                new_str = replacement + ','
            else:
                old_str = original_match
                new_str = replacement
                
            new_block = m2m_text_block.replace(old_str, new_str, 1)
            
            # Put back into lines
            block_lines = new_block.split('\n')
            lines[start_line:end_line] = block_lines
            modified = True
            print(f"  [HEALED] {os.path.basename(file_path)}:{node.lineno} -> fields.Many2many('{comodel_name}', '{rel_table}', ...)")

    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
        return True
    return False

# Scan and heal all files
print("🚀 L2 Factory Self-Healing starting...")
healed_count = 0
for root, dirs, files in os.walk(base_dir):
    # Skip standard folders
    if any(p in root for p in ('.git', '.obsidian', '.superpowers', 'mosquitto', 'config')):
        continue
    for file in files:
        if file.endswith('.py') and file != 'heal_misalignment.py':
            file_path = os.path.join(root, file)
            if heal_file(file_path):
                healed_count += 1

print(f"🎉 Self-healing execution finished. Total files healed: {healed_count}")
