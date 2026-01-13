from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestUXIntegration(TransactionCase):

    def setUp(self):
        super(TestUXIntegration, self).setUp()
        self.TermMapping = self.env['term.mapping']
        self.AccessibilitySettings = self.env['accessibility.settings']
        self.WorkspaceCustomization = self.env['workspace.customization']
        self.ContextualHelp = self.env['contextual.help']
        
        # Create a test term mapping
        self.mapping = self.TermMapping.create({
            'name': 'Test Mapping',
            'source_term': 'Manufacturing Order',
            'target_term': 'Intervention',
            'is_active': True
        })

    def test_term_mapping_logic(self):
        """Test the term mapping text replacement logic"""
        text = "This is a Manufacturing Order."
        mapped_text = self.TermMapping.apply_term_mapping_to_text(text)
        self.assertEqual(mapped_text, "This is a Intervention.")

    def test_accessibility_session_info(self):
        """Test getting accessibility features for a user"""
        settings = self.AccessibilitySettings.create({
            'name': 'User Settings',
            'user_id': self.env.user.id,
            'high_contrast_mode': True,
            'font_scaling': 1.5
        })
        
        features = self.env['accessibility.integration'].get_accessibility_features(self.env.user.id)
        self.assertTrue(features['high_contrast_mode'])
        self.assertEqual(features['font_scaling'], 1.5)

    def test_workspace_customization(self):
        """Test workspace customization retrieval"""
        custom = self.WorkspaceCustomization.create({
            'name': 'User Workspace',
            'user_id': self.env.user.id,
            'theme_preference': 'dark',
            'font_size': 'large'
        })
        
        data = self.WorkspaceCustomization.get_user_customization(self.env.user.id)
        self.assertEqual(data['theme'], 'dark')
        self.assertEqual(data['font_size'], 'large')

    def test_contextual_help_retrieval(self):
        """Test contextual help retrieval logic"""
        help_record = self.ContextualHelp.create({
            'name': 'Crop Help',
            'model_name': 'farm.crop',
            'view_type': 'form',
            'help_content': '<p>How to grow crops</p>',
            'is_active': True
        })
        
        help_data = self.env['accessibility.integration'].get_contextual_help_data('farm.crop', 'form')
        self.assertTrue(len(help_data) > 0)
        self.assertEqual(help_data[0]['name'], 'Crop Help')

    def test_term_mapping_uniqueness(self):
        """Test uniqueness constraint on term mappings"""
        with self.assertRaises(ValidationError):
            self.TermMapping.create({
                'name': 'Duplicate Mapping',
                'source_term': 'Manufacturing Order',
                'target_term': 'Action',
                'language_code': 'zh_CN'
            })
