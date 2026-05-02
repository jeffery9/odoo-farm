with open('farm_livestock/models/farm_lot.py', 'r') as f:
    content = f.read()

# Add breeding_record_id to FarmLot
if 'breeding_record_id = fields.Many2one' not in content:
    content = content.replace("dam_id = fields.Many2one('stock.lot', string='Dam')", "dam_id = fields.Many2one('stock.lot', string='Dam')\n    breeding_record_id = fields.Many2one('farm.breeding.record', string='Breeding Record')")

# Fix offspring_ids in FarmBreedingRecord
content = content.replace("# offspring_ids = fields.One2many(\n    #        .stock.lot.,\n    #        .dam_id.,\n    #        string=.Offspring.\n    #    )", "offspring_ids = fields.One2many(\n        'stock.lot',\n        'breeding_record_id',\n        string='Offspring'\n    )")

with open('farm_livestock/models/farm_lot.py', 'w') as f:
    f.write(content)
