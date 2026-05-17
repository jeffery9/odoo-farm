# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestServiceTeams(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        
        # Users & Employees
        cls.user1 = cls.env['res.users'].create({'name': 'Drone Pilot 1', 'login': 'pilot1'})
        cls.user2 = cls.env['res.users'].create({'name': 'Drone Pilot 2', 'login': 'pilot2'})
        
        cls.emp1 = cls.env['hr.employee'].create({'name': 'Drone Pilot 1', 'user_id': cls.user1.id})
        cls.emp2 = cls.env['hr.employee'].create({'name': 'Drone Pilot 2', 'user_id': cls.user2.id})
        
        # Equipment
        cls.drone = cls.env['maintenance.equipment'].create({
            'name': 'Heavy Sprayer Drone'
        })
        
        # Service Team
        cls.team = cls.env['farm.service.team'].create({
            'name': 'Elite Flying Squad',
            'leader_id': cls.emp1.id,
            'member_ids': [(4, cls.emp1.id), (4, cls.emp2.id)],
            'equipment_ids': [(4, cls.drone.id)]
        })

    def test_01_dispatch_service_team(self):
        """
        Scenario 27: Mobile Agri-Service Teams
        1. A smallholder requests a spraying task.
        2. Admin dispatches the 'Elite Flying Squad'.
        3. System automatically assigns the pilots to the task and logs the equipment dispatch.
        """
        task = self.env['project.task'].create({
            'name': 'Spraying Wheat Field for Smallholder'
        })
        
        task.action_dispatch_service_team(self.team.id)
        
        self.assertEqual(task.service_team_id.id, self.team.id, "Team must be assigned.")
        self.assertIn(self.user1, task.user_ids, "Team members must be assigned as task assignees.")
        self.assertIn(self.user2, task.user_ids, "Team members must be assigned as task assignees.")
        
        # Check logs
        messages = task.message_ids.mapped('body')
        has_eq_log = any('Heavy Sprayer Drone' in str(msg) for msg in messages)
        self.assertTrue(has_eq_log, "Dispatch log must mention the equipment sent.")

