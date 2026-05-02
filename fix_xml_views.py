import os

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.xml'):
            path = os.path.join(root, f)
            with open(path, 'r') as file:
                content = file.read()
            
            # Simple replacements for common mistakes
            content = content.replace('<name>', '<field name="name">').replace('</name>', '</field>')
            content = content.replace('<model>', '<field name="model">').replace('</model>', '</field>')
            content = content.replace('<arch type="xml">', '<field name="arch" type="xml">')
            content = content.replace('</arch>', '</field>')
            
            with open(path, 'w') as file:
                file.write(content)
