import re
import os

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.xml'):
            path = os.path.join(root, f)
            with open(path, 'r') as file:
                content = file.read()
            
            if '<xpath expr="//header" position="inside">' in content:
                def repl(m):
                    inner = m.group(1)
                    return '<xpath expr="//sheet" position="before">\n<header>\n' + inner + '\n</header>\n</xpath>'
                new_content = re.sub(r'<xpath expr="//header" position="inside">(.*?)</xpath>', repl, content, flags=re.DOTALL)
                with open(path, 'w') as file:
                    file.write(new_content)
