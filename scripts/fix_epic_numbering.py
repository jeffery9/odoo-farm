import os
import re

def renumber_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    new_lines = []
    current_num = 1
    modified = False
    
    # Pattern to match "1. **[US-..." at the start of a line
    pattern = re.compile(r'^(\d+)\. \*\*\[US-')
    
    for line in lines:
        match = pattern.match(line)
        if match:
            old_num = int(match.group(1))
            if old_num != current_num:
                new_line = re.sub(r'^\d+', str(current_num), line)
                new_lines.append(new_line)
                modified = True
            else:
                new_lines.append(line)
            current_num += 1
        else:
            new_lines.append(line)
            
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        print(f"Fixed numbering in {file_path}")
    else:
        print(f"No numbering issues in {file_path}")

epics_dir = 'docs/business/epics/'
for filename in sorted(os.listdir(epics_dir)):
    if filename.endswith('.md'):
        renumber_file(os.path.join(epics_dir, filename))
