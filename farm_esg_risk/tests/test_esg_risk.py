from odoo.tests import TransactionCase, tagged
from odoo.exceptions import ValidationError


@tagged('post_install', '-at_install')
class TestESGRisk(TransactionCase):
    """Test ESG Risk related models and functions"""

    def setUp(self):
        super().setUp()

    def test_esg_risk_assessment_creation(self):
        """Test creating an ESG risk assessment"""
        assessment = self.env['farm.esg.risk.assessment'].create({
            'name': 'Q1 2023 ESG Risk Assessment',
            'assessment_date': '2023-04-01',
            'assessment_period': 'q1',
            'year': 2023,
            'assessment_type': 'combined',
            'environmental_score': 75.0,
            'social_score': 80.0,
            'governance_score': 85.0,
            'status': 'completed'
        })

        self.assertEqual(assessment.name, 'Q1 2023 ESG Risk Assessment')
        self.assertEqual(assessment.assessment_period, 'q1')
        self.assertEqual(assessment.year, 2023)
        self.assertEqual(assessment.environmental_score, 75.0)
        self.assertEqual(assessment.social_score, 80.0)
        self.assertEqual(assessment.governance_score, 85.0)

        # Check the overall ESG score is calculated as average
        expected_overall = (75.0 + 80.0 + 85.0) / 3
        self.assertEqual(assessment.overall_esg_score, expected_overall)

        # Check the risk level is set based on the score
        self.assertEqual(assessment.esg_risk_level, 'low')  # 80.0 is in low range

    def test_esg_scores_validation(self):
        """Test that ESG scores are within 0-100 range"""
        with self.assertRaises(ValidationError):
            self.env['farm.esg.risk.assessment'].create({
                'name': 'Invalid Score Assessment',
                'assessment_date': '2023-04-01',
                'assessment_period': 'q1',
                'year': 2023,
                'assessment_type': 'combined',
                'environmental_score': 105.0,  # Invalid score > 100
                'social_score': 80.0,
                'governance_score': 85.0,
            })

        with self.assertRaises(ValidationError):
            self.env['farm.esg.risk.assessment'].create({
                'name': 'Invalid Score Assessment 2',
                'assessment_date': '2023-04-01',
                'assessment_period': 'q1',
                'year': 2023,
                'assessment_type': 'combined',
                'environmental_score': -5.0,  # Invalid score < 0
                'social_score': 80.0,
                'governance_score': 85.0,
            })

    def test_esg_compliance_monitoring_creation(self):
        """Test creating an ESG compliance monitoring record"""
        compliance = self.env['farm.esg.compliance.monitoring'].create({
            'name': 'Waste Management Compliance Check',
            'compliance_type': 'environmental',
            'regulation_reference': 'Environmental Protection Act',
            'threshold_value': 95.0,
            'current_value': 97.0,
            'last_check_date': '2023-06-01',
            'next_check_date': '2023-09-01'
        })

        self.assertEqual(compliance.name, 'Waste Management Compliance Check')
        self.assertEqual(compliance.compliance_type, 'environmental')
        self.assertEqual(compliance.regulation_reference, 'Environmental Protection Act')
        self.assertEqual(compliance.threshold_value, 95.0)
        self.assertEqual(compliance.current_value, 97.0)

        # Since current value is above threshold, compliance status should be compliant
        self.assertEqual(compliance.compliance_status, 'compliant')

    def test_compliance_status_computation(self):
        """Test the compliance status computation logic"""
        # Test compliant status (current <= threshold)
        compliant_record = self.env['farm.esg.compliance.monitoring'].create({
            'name': 'Compliant Record',
            'compliance_type': 'regulatory',
            'threshold_value': 80.0,
            'current_value': 75.0,
        })
        self.assertEqual(compliant_record.compliance_status, 'compliant')

        # Test warning status (threshold < current <= threshold * 1.1)
        warning_record = self.env['farm.esg.compliance.monitoring'].create({
            'name': 'Warning Record',
            'compliance_type': 'regulatory',
            'threshold_value': 80.0,
            'current_value': 84.0,  # 84.0 is between 80.0 and 88.0 (80*1.1)
        })
        self.assertEqual(warning_record.compliance_status, 'warning')

        # Test non_compliant status (threshold*1.1 < current <= threshold * 1.3)
        non_compliant_record = self.env['farm.esg.compliance.monitoring'].create({
            'name': 'Non-Compliant Record',
            'compliance_type': 'regulatory',
            'threshold_value': 80.0,
            'current_value': 95.0,  # 95.0 is between 88.0 and 104.0 (80*1.3)
        })
        self.assertEqual(non_compliant_record.compliance_status, 'non_compliant')

        # Test critical status (current > threshold * 1.3)
        critical_record = self.env['farm.esg.compliance.monitoring'].create({
            'name': 'Critical Record',
            'compliance_type': 'regulatory',
            'threshold_value': 80.0,
            'current_value': 110.0,  # 110.0 is > 104.0 (80*1.3)
        })
        self.assertEqual(critical_record.compliance_status, 'critical')

    def test_esg_data_governance_creation(self):
        """Test creating an ESG data governance record"""
        data_governance = self.env['farm.esg.data.governance'].create({
            'name': 'Carbon Footprint Data Governance',
            'data_source': 'Carbon Tracking System',
            'data_type': 'environmental',
            'collection_method': 'automated',
            'data_owner': self.env.user.id,
            'data_quality_score': 92.0,
            'validation_status': 'validated',
            'data_security_classification': 'internal'
        })

        self.assertEqual(data_governance.name, 'Carbon Footprint Data Governance')
        self.assertEqual(data_governance.data_source, 'Carbon Tracking System')
        self.assertEqual(data_governance.data_type, 'environmental')
        self.assertEqual(data_governance.data_quality_score, 92.0)

    def test_data_quality_validation(self):
        """Test the data quality validation functionality"""
        data_governance = self.env['farm.esg.data.governance'].create({
            'name': 'Test Data Governance',
            'data_source': 'Test System',
            'data_type': 'social',
            'collection_method': 'manual',
            'validation_status': 'pending'
        })

        # Test validation method
        data_governance.action_validate_data()

        # Since no data_owner was initially set, quality score should be reduced
        self.assertLess(data_governance.data_quality_score, 100)
        self.assertIn(data_governance.validation_status, ['validated', 'requires_review'])

    def test_stakeholder_engagement_creation(self):
        """Test creating a stakeholder engagement record"""
        partner = self.env['res.partner'].create({
            'name': 'Local Community Group',
            'is_company': False,
        })

        engagement = self.env['farm.esg.stakeholder.engagement'].create({
            'name': 'Community Meeting on Water Usage',
            'stakeholder_id': partner.id,
            'stakeholder_type': 'community',
            'engagement_date': '2023-08-15',
            'engagement_type': 'meeting',
            'engagement_topic': 'environmental_impact',
            'participants_count': 45,
            'outcome_summary': 'Discussed water conservation measures',
            'engagement_score': 85.0,
            'satisfaction_rating': 'satisfied',
            'follow_up_required': True,
            'report_year': 2023
        })

        self.assertEqual(engagement.name, 'Community Meeting on Water Usage')
        self.assertEqual(engagement.stakeholder_type, 'community')
        self.assertEqual(engagement.engagement_type, 'meeting')
        self.assertEqual(engagement.participants_count, 45)
        self.assertTrue(engagement.follow_up_required)

    def test_engagement_follow_up_required(self):
        """Test the follow up required logic based on satisfaction rating"""
        partner = self.env['res.partner'].create({
            'name': 'Dissatisfied Stakeholder',
            'is_company': False,
        })

        engagement = self.env['farm.esg.stakeholder.engagement'].create({
            'name': 'Satisfaction Survey',
            'stakeholder_id': partner.id,
            'stakeholder_type': 'community',
            'engagement_date': '2023-08-15',
            'engagement_type': 'survey',
            'satisfaction_rating': 'dissatisfied',
        })

        # Initially follow up might not be required
        self.assertFalse(engagement.follow_up_required)

        # Now test the method that marks follow-up as required
        engagement.action_follow_up_required()
        # It should only mark as required if satisfaction is low
        if engagement.satisfaction_rating in ['dissatisfied', 'very_dissatisfied']:
            self.assertTrue(engagement.follow_up_required)

    def test_esg_kpi_creation(self):
        """Test creating an ESG KPI record"""
        hr_department = self.env['hr.department'].create({
            'name': 'Sustainability Department',
        })

        kpi = self.env['farm.esg.kpi'].create({
            'name': 'Carbon Emission Reduction',
            'kpi_category': 'environmental',
            'kpi_type': 'carbon_emissions',
            'reporting_period': 'annual',
            'target_value': 1000.0,
            'current_value': 850.0,
            'baseline_value': 1200.0,
            'unit_of_measurement': 'tCO2e',
            'responsible_department': hr_department.id,
            'year': 2023
        })

        self.assertEqual(kpi.name, 'Carbon Emission Reduction')
        self.assertEqual(kpi.kpi_category, 'environmental')
        self.assertEqual(kpi.kpi_type, 'carbon_emissions')
        self.assertEqual(kpi.target_value, 1000.0)
        self.assertEqual(kpi.current_value, 850.0)

        # Check that achievement percentage is calculated
        expected_achievement = (850.0 / 1000.0) * 100  # 85.0%
        self.assertEqual(kpi.achievement_percentage, expected_achievement)

        # Check that performance status is calculated
        self.assertEqual(kpi.performance_status, 'on_track')  # 85% is on track

    def test_kpi_performance_status_calculation(self):
        """Test the performance status calculation for different achievement percentages"""
        # Create KPI with 100% achievement
        kpi_100 = self.env['farm.esg.kpi'].create({
            'name': '100% Achievement KPI',
            'kpi_category': 'environmental',
            'target_value': 100.0,
            'current_value': 100.0,
            'unit_of_measurement': 'units',
            'year': 2023
        })
        self.assertEqual(kpi_100.performance_status, 'exceeding')

        # Create KPI with 85% achievement
        kpi_85 = self.env['farm.esg.kpi'].create({
            'name': '85% Achievement KPI',
            'kpi_category': 'environmental',
            'target_value': 100.0,
            'current_value': 85.0,
            'unit_of_measurement': 'units',
            'year': 2023
        })
        self.assertEqual(kpi_85.performance_status, 'on_track')

        # Create KPI with 70% achievement
        kpi_70 = self.env['farm.esg.kpi'].create({
            'name': '70% Achievement KPI',
            'kpi_category': 'environmental',
            'target_value': 100.0,
            'current_value': 70.0,
            'unit_of_measurement': 'units',
            'year': 2023
        })
        self.assertEqual(kpi_70.performance_status, 'at_risk')

        # Create KPI with 40% achievement
        kpi_40 = self.env['farm.esg.kpi'].create({
            'name': '40% Achievement KPI',
            'kpi_category': 'environmental',
            'target_value': 100.0,
            'current_value': 40.0,
            'unit_of_measurement': 'units',
            'year': 2023
        })
        self.assertEqual(kpi_40.performance_status, 'off_track')