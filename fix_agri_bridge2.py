import re
with open('agri_precision_core/views/precision_bridge_views.xml', 'r') as f:
    content = f.read()

# Just put the xpath back to `//sheet` with `position="inside"` without any nested `<notebook>` unless we actually add one AND close it correctly.
# Currently: `<!-- IoT Section for Stock Lot -->`
# Then: `<xpath expr="//notebook" position="inside">`
# Let's see what is currently there.
