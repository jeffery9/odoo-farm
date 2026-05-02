import os

for root, dirs, files in os.walk('.'):
    if '__manifest__.py' in files:
        path = os.path.join(root, '__manifest__.py')
        with open(path, 'r') as f:
            content = f.read()
            
        if "'views/menu.xml'," in content or '"views/menu.xml",' in content:
            lines = content.split('\n')
            new_lines = []
            menu_line = None
            last_view_idx = -1
            
            for line in lines:
                if "'views/menu.xml'," in line or '"views/menu.xml",' in line:
                    menu_line = line
                else:
                    new_lines.append(line)
            
            if menu_line:
                for i, line in enumerate(new_lines):
                    if "'views/" in line or '"views/' in line:
                        last_view_idx = i
                
                if last_view_idx != -1:
                    new_lines.insert(last_view_idx + 1, menu_line)
                else:
                    new_lines.append(menu_line)
                    
            new_content = '\n'.join(new_lines)
            if new_content != content:
                with open(path, 'w') as f:
                    f.write(new_content)
