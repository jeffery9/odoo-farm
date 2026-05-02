with open('farm_ai_agent/__manifest__.py', 'r') as f:
    content = f.read()

content = content.replace('"farm_ai_llm_integration",', '"farm_ai_llm_integration",\n        "farm_robotics",')

with open('farm_ai_agent/__manifest__.py', 'w') as f:
    f.write(content)
