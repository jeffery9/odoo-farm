from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestTrainingAccess(TransactionCase):

    def setUp(self):
        super(TestTrainingAccess, self).setUp()
        self.Employee = self.env['hr.employee']
        self.CertType = self.env['farm.certificate.type']
        self.Cert = self.env['farm.certificate']
        self.Intervention = self.env['mrp.production']
        
        # 1. Create a certificate type for Drone/Protection
        self.drone_cert_type = self.CertType.create({
            'name': 'Drone License',
            'code': 'DRONE',
            'required_for_intervention_types': 'protection'
        })
        
        # 2. Create employees
        self.worker_qualified = self.Employee.create({'name': 'Qualified Pilot'})
        self.worker_unqualified = self.Employee.create({'name': 'Normal Worker'})
        
        # 3. Give certificate to one worker
        self.Cert.create({
            'name': 'CERT-001',
            'employee_id': self.worker_qualified.id,
            'certificate_type_id': self.drone_cert_type.id,
            'expiry_date': '2099-01-01' # Valid
        })

    def test_01_qualification_check(self):
        """ Test that only qualified workers can confirm protection tasks [US-17-08] """
        # Create a protection intervention
        mo = self.Intervention.create({
            'product_id': self.env.ref('product.product_delivery_01', raise_if_not_found=False).id or 1,
            'product_qty': 1.0,
            'intervention_type': 'protection',
            'doer_ids': [(6, 0, [self.worker_unqualified.id])]
        })
        
        # Confirmation should fail for unqualified worker
        with self.assertRaises(UserError):
            mo.action_confirm()
            
        # Change to qualified worker
        mo.write({'doer_ids': [(6, 0, [self.worker_qualified.id])]})
        mo.action_confirm()
        self.assertEqual(mo.state, 'confirmed')
