import re
with open('farm_processing/models/stock_lot.py', 'r') as f:
    content = f.read()

content = content.replace("# plot_id = fields.Many2one('farm.land', string='Origin Plot')", "plot_id = fields.Many2one('farm.location', string='Origin Plot')")

with open('farm_processing/models/stock_lot.py', 'w') as f:
    f.write(content)
