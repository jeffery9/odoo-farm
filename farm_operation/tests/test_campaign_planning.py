from odoo.tests.common import TransactionCase

class TestCampaignPlanning(TransactionCase):

    def setUp(self):
        super(TestCampaignPlanning, self).setUp()
        self.Campaign = self.env['agricultural.campaign']
        self.Task = self.env['project.task']
        self.Project = self.env['project.project']
        
        self.agri_project = self.Project.create({
            'name': 'Planting Project',
            'is_agri_activity': True,
            'activity_family': 'planting'
        })

    def test_01_create_campaign(self):
        """ 测试创建生产季 [US-05] """
        campaign = self.Campaign.create({
            'name': '2026 Spring Season',
            'date_start': '2026-03-01',
            'date_end': '2026-06-30'
        })
        self.assertEqual(campaign.name, '2026 Spring Season')

    def test_02_task_link_to_campaign(self):
        """ 测试生产任务关联生产季 [US-05] """
        campaign = self.Campaign.create({'name': '2026 Summer'})
        task = self.Task.create({
            'name': 'Wheat Production Task - Plot 01',
            'project_id': self.agri_project.id,
            'campaign_id': campaign.id
        })
        self.assertEqual(task.campaign_id.id, campaign.id, "任务应正确关联生产季")
