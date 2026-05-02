with open('farm_apiculture/views/apiculture_operation_views.xml', 'r') as f:
    content = f.read()

# Remove the inheritance, just create a new form view for farm.hive.inspection
content = content.replace('<field name="model">project.task</field>', '<field name="model">farm.hive.inspection</field>')
content = content.replace('<field name="inherit_id" ref="project.view_task_form2"/>', '')
content = content.replace('<xpath expr="//page[@name=\'extra_info\']" position="after">', '<form><sheet><notebook>')
content = content.replace('</xpath>', '</notebook></sheet></form>')

with open('farm_apiculture/views/apiculture_operation_views.xml', 'w') as f:
    f.write(content)
