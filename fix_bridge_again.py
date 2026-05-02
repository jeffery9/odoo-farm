with open('agri_precision_core/views/precision_bridge_views.xml', 'r') as f:
    content = f.read()

# Restore it and correctly add notebook opening and closing
# Or maybe the first `//sheet` inside `mrp.production` should not be `<notebook>`?
# It should just be inside sheet.
# The original code:
# <xpath expr="//div[@name='button_box']" position="inside"> ... </xpath>
# Let's restore the original and apply the CORRECT fix!
