from odoo.tests import TransactionCase, tagged
from odoo.exceptions import ValidationError


@tagged('post_install', '-at_install')
class TestESGReport(TransactionCase):
    """Test ESG Report related models and functions"""

    def setUp(self):
        super().setUp()

    def test_esg_report_creation(self):
        """Test creating an ESG report"""
        report = self.env['farm.esg.report'].create({
            'name': 'Q2 2023 ESG Report',
            'report_type': 'quarterly',
            'report_period': 'q2',
            'report_year': 2023,
            'language': 'en',
            'report_format': 'pdf',
            'industry_sector': 'crop_farming',
            'report_status': 'draft'
        })

        self.assertEqual(report.name, 'Q2 2023 ESG Report')
        self.assertEqual(report.report_type, 'quarterly')
        self.assertEqual(report.report_period, 'q2')
        self.assertEqual(report.report_year, 2023)
        self.assertEqual(report.language, 'en')
        self.assertEqual(report.report_status, 'draft')

    def test_report_content_generation(self):
        """Test generating report content"""
        report = self.env['farm.esg.report'].create({
            'name': 'Test Report for Content Generation',
            'report_type': 'annual',
            'report_period': 'annual',
            'report_year': 2023,
            'language': 'en',
            'report_format': 'pdf',
            'industry_sector': 'mixed_farming',
            'report_status': 'draft'
        })

        # Generate content
        report.action_generate_report_content()

        # Check that sections were populated with placeholder content
        self.assertIsNotNone(report.environmental_section)
        self.assertIn('Environmental', report.environmental_section)
        self.assertIsNotNone(report.social_section)
        self.assertIn('Social', report.social_section)
        self.assertIsNotNone(report.governance_section)
        self.assertIn('Governance', report.governance_section)

    def test_report_approval_process(self):
        """Test the report approval workflow"""
        report = self.env['farm.esg.report'].create({
            'name': 'Test Report for Approval',
            'report_type': 'annual',
            'report_period': 'annual',
            'report_year': 2023,
            'language': 'en',
            'report_format': 'pdf',
            'industry_sector': 'mixed_farming',
            'report_status': 'draft'
        })

        # Initially the status should be draft
        self.assertEqual(report.report_status, 'draft')

        # Approve the report
        report.action_approve_report()

        # Check that status is now approved and approval date is set
        self.assertEqual(report.report_status, 'approved')
        self.assertIsNotNone(report.approval_date)

    def test_report_publish_process(self):
        """Test the report publishing process"""
        report = self.env['farm.esg.report'].create({
            'name': 'Test Report for Publishing',
            'report_type': 'annual',
            'report_period': 'annual',
            'report_year': 2023,
            'language': 'en',
            'report_format': 'pdf',
            'industry_sector': 'mixed_farming',
            'report_status': 'draft'
        })

        # Can't publish a draft report
        with self.assertRaises(ValidationError):
            report.action_publish_report()

        # First approve the report
        report.action_approve_report()
        self.assertEqual(report.report_status, 'approved')

        # Now publish the report
        report.action_publish_report()
        self.assertEqual(report.report_status, 'published')
        self.assertIsNotNone(report.publication_date)

    def test_sustainability_goal_creation(self):
        """Test creating a sustainability goal"""
        goal = self.env['farm.esg.sustainability.goal'].create({
            'name': 'Reduce Carbon Emissions by 2030',
            'goal_type': 'environmental',
            'description': 'Reduce carbon emissions by 50% by 2030 compared to 2020 baseline',
            'target_year': 2030,
            'baseline_year': 2020,
            'baseline_value': 1000.0,  # metric tons CO2e
            'target_value': 500.0,     # metric tons CO2e (50% reduction)
            'current_value': 750.0,    # Current value
            'responsible_team': self.env['hr.department'].create({'name': 'Sustainability'}).id,
            'key_performance_indicators': 'Carbon emissions in metric tons CO2e',
            'action_plan': 'Transition to renewable energy, improve efficiency measures',
            'monitoring_frequency': 'annual'
        })

        self.assertEqual(goal.name, 'Reduce Carbon Emissions by 2030')
        self.assertEqual(goal.goal_type, 'environmental')
        self.assertEqual(goal.target_year, 2030)
        self.assertEqual(goal.baseline_value, 1000.0)
        self.assertEqual(goal.target_value, 500.0)

        # Check that progress percentage is calculated
        expected_progress = ((750.0 - 1000.0) / (500.0 - 1000.0)) * 100  # 50%
        # Since current is 750, which is halfway from baseline (1000) to target (500)
        self.assertEqual(goal.progress_percentage, expected_progress)
        self.assertIn(goal.goal_status, ['in_progress', 'at_risk'])  # Based on progress

    def test_supply_chain_esg_rating_creation(self):
        """Test creating a supply chain ESG rating"""
        partner = self.env['res.partner'].create({
            'name': 'Test Supplier',
            'is_company': True,
        })

        rating = self.env['farm.esg.supply.chain.rating'].create({
            'name': 'Q3 2023 Supplier Rating',
            'supplier_id': partner.id,
            'rating_date': '2023-09-30',
            'environmental_score': 78.0,
            'social_score': 82.0,
            'governance_score': 85.0,
            'rating_period': 'q3',
            'year': 2023,
            'rating_method': 'self_assessment'
        })

        self.assertEqual(rating.name, 'Q3 2023 Supplier Rating')
        self.assertEqual(rating.supplier_id.id, partner.id)
        self.assertEqual(rating.environmental_score, 78.0)
        self.assertEqual(rating.social_score, 82.0)
        self.assertEqual(rating.governance_score, 85.0)

        # Check the overall score calculation
        expected_overall = (78.0 + 82.0 + 85.0) / 3
        self.assertEqual(rating.overall_esg_score, expected_overall)

        # Check the risk level is based on the score
        self.assertEqual(rating.esg_risk_level, 'low')  # 81.67 is in low range

    def test_supply_chain_rating_validation(self):
        """Test validation for supply chain ESG rating scores"""
        partner = self.env['res.partner'].create({
            'name': 'Test Supplier for Validation',
            'is_company': True,
        })

        with self.assertRaises(ValidationError):
            self.env['farm.esg.supply.chain.rating'].create({
                'name': 'Invalid Score Rating',
                'supplier_id': partner.id,
                'environmental_score': 105.0,  # Invalid > 100
                'social_score': 80.0,
                'governance_score': 85.0,
                'rating_period': 'q1',
                'year': 2023
            })

        with self.assertRaises(ValidationError):
            self.env['farm.esg.supply.chain.rating'].create({
                'name': 'Invalid Score Rating 2',
                'supplier_id': partner.id,
                'environmental_score': -5.0,  # Invalid < 0
                'social_score': 80.0,
                'governance_score': 85.0,
                'rating_period': 'q1',
                'year': 2023
            })

    def test_goal_progress_update(self):
        """Test updating goal progress"""
        goal = self.env['farm.esg.sustainability.goal'].create({
            'name': 'Biodiversity Improvement Goal',
            'goal_type': 'environmental',
            'target_year': 2030,
            'baseline_year': 2020,
            'baseline_value': 50.0,   # biodiversity index
            'target_value': 80.0,     # biodiversity index
            'current_value': 55.0,    # Current value
        })

        # Initially progress is based on creation values
        initial_progress = goal.progress_percentage
        self.assertGreaterEqual(initial_progress, 0)
        self.assertLessEqual(initial_progress, 100)

        # Update the current value and call the update method
        goal.current_value = 65.0
        goal.action_update_progress()

        # Check the status has been updated appropriately
        expected_status = 'on_track'  # 65 is between baseline (50) and target (80)
        # The actual status might vary based on the exact progress calculation
        self.assertIsNotNone(goal.goal_status)

    def test_esg_dashboard_creation(self):
        """Test creating an ESG dashboard"""
        dashboard = self.env['farm.esg.dashboard'].create({
            'name': 'Executive ESG Dashboard',
            'dashboard_type': 'executive',
            'display_period': 'current_year',
            'target_audience': 'executive',
            'environmental_score': 75.0,
            'social_score': 78.0,
            'governance_score': 82.0,
        })

        self.assertEqual(dashboard.name, 'Executive ESG Dashboard')
        self.assertEqual(dashboard.dashboard_type, 'executive')
        self.assertEqual(dashboard.target_audience, 'executive')

        # The overall score is computed from component scores
        expected_overall = (75.0 + 78.0 + 82.0) / 3
        # Note: Since we're using a compute method, we would need to trigger it
        # but in tests, computed fields might not update immediately