from odoo.tests.common import TransactionCase

class TestBreedingManagement(TransactionCase):

    def setUp(self):
        super(TestBreedingManagement, self).setUp()
        self.Lot = self.env['stock.lot']
        self.Product = self.env['product.product']
        self.Trait = self.env['farm.trait.value']
        
        self.variety = self.Product.create({
            'name': 'Super Tomato V1',
            'type': 'product',
            'is_variety': True
        })

    def test_01_pedigree_tracking(self):
        """ 测试系谱追踪（父母本关联） [US-10-02] """
        father = self.Lot.create({'name': 'TOM-MALE-01', 'product_id': self.variety.id, 'gender': 'male'})
        mother = self.Lot.create({'name': 'TOM-FEMALE-01', 'product_id': self.variety.id, 'gender': 'female'})
        
        offspring = self.Lot.create({
            'name': 'TOM-OFFSPRING-01',
            'product_id': self.variety.id,
            'father_id': father.id,
            'mother_id': mother.id
        })
        
        self.assertEqual(offspring.father_id.id, father.id)
        self.assertEqual(offspring.mother_id.id, mother.id)

    def test_02_trait_recording(self):
        """ 测试性状指标记录 [US-10-02] """
        lot = self.Lot.create({'name': 'TOM-TRAIT-01', 'product_id': self.variety.id})
        
        # 记录性状：抗病性=高
        trait_val = self.Trait.create({
            'lot_id': lot.id,
            'name': 'Disease Resistance',
            'value': 'High',
            'score': 9.5
        })
        
        self.assertEqual(lot.trait_value_ids[0].value, 'High')
        self.assertEqual(lot.trait_score_avg, 9.5)
