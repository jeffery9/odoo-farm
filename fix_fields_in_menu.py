import os

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.xml'):
            path = os.path.join(root, f)
            with open(path, 'r') as file:
                content = file.read()
                
            content = content.replace('<view_mode>', '<field name="view_mode">').replace('</view_mode>', '</field>')
            content = content.replace('<res_model>', '<field name="res_model">').replace('</res_model>', '</field>')
            
            with open(path, 'w') as file:
                file.write(content)
