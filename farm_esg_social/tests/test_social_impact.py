from odoo.tests import TransactionCase, tagged
from odoo.exceptions import ValidationError


@tagged('post_install', '-at_install')
class TestSocialImpact(TransactionCase):
    """Test Social Impact related models and functions"""

    def setUp(self):
        super().setUp()

        # Create test employee for labor condition testing
        self.employee = self.env['hr.employee'].create({
            'name': 'John Doe',
            'work_location': 'Farm A',
        })

        # Create test partner for community investment
        self.partner = self.env['res.partner'].create({
            'name': 'Test Community Partner',
            'is_company': False,
        })

    def test_community_investment_creation(self):
        """Test creating a community investment record"""
        investment = self.env['farm.esg.community.investment'].create({
            'name': 'Test Community Investment',
            'investment_type': 'infrastructure',
            'amount': 10000.0,
            'beneficiaries_count': 100,
            'location': 'Test Location',
            'investment_date': '2023-06-01',
            'project_status': 'planned'
        })

        self.assertEqual(investment.name, 'Test Community Investment')
        self.assertEqual(investment.investment_type, 'infrastructure')
        self.assertEqual(investment.amount, 10000.0)
        self.assertEqual(investment.beneficiaries_count, 100)

    def test_community_investment_dates_validation(self):
        """Test validation of investment dates"""
        with self.assertRaises(ValidationError):
            self.env['farm.esg.community.investment'].create({
                'name': 'Test Invalid Date Investment',
                'investment_type': 'education',
                'amount': 5000.0,
                'investment_date': '2023-06-01',
                'start_date': '2023-06-15',
                'end_date': '2023-06-10',  # End date before start date
            })

    def test_annual_community_investments(self):
        """Test retrieving annual community investments"""
        # Create multiple investments for different years
        self.env['farm.esg.community.investment'].create({
            'name': '2023 Investment',
            'investment_type': 'education',
            'amount': 5000.0,
            'investment_date': '2023-06-01',
            'report_year': 2023
        })

        self.env['farm.esg.community.investment'].create({
            'name': '2024 Investment',
            'investment_type': 'healthcare',
            'amount': 8000.0,
            'investment_date': '2024-03-01',
            'report_year': 2024
        })

        # Test the get_annual_community_investments method
        result_2023 = self.env['farm.esg.community.investment'].get_annual_community_investments(2023)
        self.assertEqual(result_2023['total_amount'], 5000.0)
        self.assertEqual(result_2023['count'], 1)

        result_2024 = self.env['farm.esg.community.investment'].get_annual_community_investments(2024)
        self.assertEqual(result_2024['total_amount'], 8000.0)
        self.assertEqual(result_2024['count'], 1)

    def test_labor_condition_creation(self):
        """Test creating a labor condition record"""
        labor_condition = self.env['farm.esg.labor.condition'].create({
            'name': 'Safety Training Certificate',
            'employee_id': self.employee.id,
            'condition_type': 'safety_training',
            'issue_date': '2023-01-01',
            'expiry_date': '2024-01-01',
            'certification': 'OSHA Safety Training',
            'issuing_body': 'Occupational Safety and Health Administration',
            'compliance_status': 'compliant'
        })

        self.assertEqual(labor_condition.name, 'Safety Training Certificate')
        self.assertEqual(labor_condition.employee_id.id, self.employee.id)
        self.assertEqual(labor_condition.condition_type, 'safety_training')
        self.assertTrue(labor_condition.is_valid)

    def test_labor_condition_expiry(self):
        """Test labor condition expiry status"""
        # Create an expired condition
        expired_condition = self.env['farm.esg.labor.condition'].create({
            'name': 'Expired Safety Training',
            'employee_id': self.employee.id,
            'condition_type': 'safety_training',
            'issue_date': '2020-01-01',
            'expiry_date': '2021-01-01',  # Expired
            'certification': 'OSHA Safety Training',
            'issuing_body': 'Occupational Safety and Health Administration',
            'compliance_status': 'expired'
        })

        self.assertFalse(expired_condition.is_valid)

    def test_supply_chain_diversity_creation(self):
        """Test creating a supply chain diversity record"""
        partner = self.env['res.partner'].create({
            'name': 'Local Supplier',
            'is_company': True,
            'country_id': self.env.ref('base.cn').id,  # China
        })

        # Create a company with China as country to make supplier local
        company = self.env.company
        company.country_id = self.env.ref('base.cn').id

        diversity_record = self.env['farm.esg.supply.chain.diversity'].create({
            'name': 'Local Supplier Engagement',
            'supplier_id': partner.id,
            'supplier_type': 'local',
            'procurement_amount': 20000.0,
            'procurement_percentage': 25.0,
            'report_year': 2023
        })

        self.assertEqual(diversity_record.name, 'Local Supplier Engagement')
        self.assertTrue(diversity_record.local_supplier)

    def test_small_holder_empowerment_creation(self):
        """Test creating a small holder empowerment record"""
        empowerment = self.env['farm.esg.small.holder.empowerment'].create({
            'name': 'Training on Modern Farming Techniques',
            'farmer_id': self.partner.id,
            'activity_type': 'training',
            'activity_date': '2023-05-15',
            'training_topic': 'Crop Management',
            'participants_count': 25,
            'duration_hours': 8.0,
            'location': 'Training Center A',
            'productivity_impact': 15.0,
            'adoption_rate': 80.0,
            'follow_up_required': True
        })

        self.assertEqual(empowerment.name, 'Training on Modern Farming Techniques')
        self.assertEqual(empowerment.activity_type, 'training')
        self.assertEqual(empowerment.training_topic, 'Crop Management')
        self.assertEqual(empowerment.productivity_impact, 15.0)

    def test_community_health_impact_creation(self):
        """Test creating a community health impact assessment"""
        health_impact = self.env['farm.esg.community.health.impact'].create({
            'name': 'Pesticide Impact Assessment',
            'assessment_date': '2023-07-01',
            'assessment_type': 'pesticide_impact',
            'location': 'Village A',
            'affected_population': 500,
            'impact_level': 'medium',
            'exposure_risk_level': 65.0,
            'health_indicator': 'respiratory',
            'mitigation_measures': 'Provide masks and training',
            'measure_effectiveness': 'effective',
            'mitigation_cost': 1500.0,
            'report_year': 2023
        })

        self.assertEqual(health_impact.name, 'Pesticide Impact Assessment')
        self.assertEqual(health_impact.assessment_type, 'pesticide_impact')
        self.assertEqual(health_impact.impact_level, 'medium')
        self.assertEqual(health_impact.affected_population, 500)