# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class TestGenomicBreeding(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        
        cls.pig_product = cls.env['product.product'].create({
            'name': 'Breeding Pig',
            'type': 'product',
            'tracking': 'lot'
        })
        
        # Grandparents
        cls.gp_male = cls.env['stock.lot'].create({
            'name': 'GP-MALE', 'product_id': cls.pig_product.id, 'company_id': cls.env.company.id, 'gender': 'male', 'dna_marker': 'GENE-X'
        })
        cls.gp_female = cls.env['stock.lot'].create({
            'name': 'GP-FEM', 'product_id': cls.pig_product.id, 'company_id': cls.env.company.id, 'gender': 'female', 'dna_marker': 'GENE-NORMAL'
        })
        
        # Sire and Dam (Half-siblings or carrying lethal genes)
        cls.sire = cls.env['stock.lot'].create({
            'name': 'SIRE-01', 'product_id': cls.pig_product.id, 'company_id': cls.env.company.id, 'gender': 'male',
            'father_id': cls.gp_male.id, 'mother_id': cls.gp_female.id, 'dna_marker': 'LETHAL-RECESSIVE'
        })
        cls.dam = cls.env['stock.lot'].create({
            'name': 'DAM-01', 'product_id': cls.pig_product.id, 'company_id': cls.env.company.id, 'gender': 'female',
            'father_id': cls.gp_male.id, 'mother_id': cls.gp_female.id, 'dna_marker': 'LETHAL-RECESSIVE'
        })
        
        cls.safe_sire = cls.env['stock.lot'].create({
            'name': 'SAFE-SIRE', 'product_id': cls.pig_product.id, 'company_id': cls.env.company.id, 'gender': 'male',
            'dna_marker': 'GENE-NORMAL'
        })

    def test_01_inbreeding_block(self):
        """
        Scenario:
        1. Attempt to create a mating order between Sire-01 and Dam-01.
        2. System detects they share the same father (GP-MALE), risking inbreeding.
        3. Mating is blocked via UserError.
        """
        with self.assertRaises(UserError) as e:
            self.env['farm.nursery.batch'].create({
                'name': 'Inbreeding Batch',
                'product_id': self.pig_product.id,
                'parent_p1_id': self.sire.id,
                'parent_p2_id': self.dam.id,
                'company_id': self.env.company.id,
            })
        self.assertIn("Inbreeding Risk", str(e.exception))

    def test_02_lethal_gene_collision_block(self):
        """
        Scenario:
        1. Attempt to mate two animals that don't share ancestors but carry the same lethal recessive gene.
        2. Mating is blocked.
        """
        alien_dam = self.env['stock.lot'].create({
            'name': 'ALIEN-DAM', 'product_id': self.pig_product.id, 'company_id': self.env.company.id, 'gender': 'female',
            'dna_marker': 'LETHAL-RECESSIVE'
        })
        with self.assertRaises(UserError) as e:
            self.env['farm.nursery.batch'].create({
                'name': 'Lethal Batch',
                'product_id': self.pig_product.id,
                'parent_p1_id': self.sire.id,
                'parent_p2_id': alien_dam.id,
                'company_id': self.env.company.id,
            })
        self.assertIn("Lethal Gene Collision", str(e.exception))
        
    def test_03_successful_mating_trait_inheritance(self):
        """
        Scenario:
        1. Safe mating occurs.
        2. Offspring automatically calculates combined genetic traits.
        """
        self.sire.write({'trait_value_ids': [(0, 0, {'name': 'Meat Yield', 'score': 8.0})]})
        alien_safe_dam = self.env['stock.lot'].create({
            'name': 'SAFE-DAM', 'product_id': self.pig_product.id, 'company_id': self.env.company.id, 'gender': 'female',
            'dna_marker': 'GENE-NORMAL',
            'trait_value_ids': [(0, 0, {'name': 'Meat Yield', 'score': 9.0})]
        })
        
        batch = self.env['farm.nursery.batch'].create({
            'name': 'Success Batch',
            'product_id': self.pig_product.id,
            'parent_p1_id': self.sire.id,
            'parent_p2_id': alien_safe_dam.id,
            'company_id': self.env.company.id,
        })
        
        # Verify inherited score is average of parents (8.5)
        meat_yield_trait = batch.lot_id.trait_value_ids.filtered(lambda t: t.name == 'Meat Yield')
        self.assertTrue(meat_yield_trait, "Offspring must inherit traits from parents.")
        self.assertEqual(meat_yield_trait.score, 8.5, "Inherited score should be average of parents.")

