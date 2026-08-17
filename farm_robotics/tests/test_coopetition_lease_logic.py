# -*- coding: utf-8 -*-
# filepath: odoo-farm-dev/farm_robotics/tests/test_coopetition_lease_logic.py
from odoo.tests.common import TransactionCase
from odoo.tests import tagged
from odoo import fields
from datetime import timedelta

@tagged('post_install', '-at_install')
class TestCoopetitionLeaseLogic(TransactionCase):

    def setUp(self):
        super(TestCoopetitionLeaseLogic, self).setUp()
        self.LocationModel = self.env['farm.location']
        
        # Search or create base locations & robots
        self.location = self.LocationModel.create({
            'name': 'BDD Field North (测试北地块)',
            'location_type': 'field'
        })
        self.robot_a = self.env['farm.robot'].create({
            'name': 'Scout Drone A',
            'robot_type': 'scout'
        })
        self.robot_b = self.env['farm.robot'].create({
            'name': 'Scout Drone B',
            'robot_type': 'scout'
        })

    def test_01_immediate_acquisition_and_queuing(self):
        """ Immediate lease on idle field, second request queued """
        now = fields.Datetime.now()
        
        # 1. Scout-A requests lease
        lease_a = self.env['agri.robotics.lease'].create({
            'res_model': 'farm.location',
            'res_id': self.location.id,
            'robot_id': self.robot_a.id,
            'expiration_date': now + timedelta(hours=2),
            'state': 'draft'
        })
        lease_a.action_request_lease()
        self.assertEqual(lease_a.state, 'active', "First lease on idle resource must be set to 'active'")

        # 2. Scout-B requests lease during the same time
        lease_b = self.env['agri.robotics.lease'].create({
            'res_model': 'farm.location',
            'res_id': self.location.id,
            'robot_id': self.robot_b.id,
            'expiration_date': now + timedelta(hours=1),
            'state': 'draft'
        })
        lease_b.action_request_lease()
        self.assertEqual(lease_b.state, 'queued', "Lease request on busy resource must be set to 'queued'")

    def test_02_wakeup_chain_on_release(self):
        """ Releasing lease A must wake up queued lease B """
        now = fields.Datetime.now()
        lease_a = self.env['agri.robotics.lease'].create({
            'res_model': 'farm.location',
            'res_id': self.location.id,
            'robot_id': self.robot_a.id,
            'expiration_date': now + timedelta(hours=2),
            'state': 'active'
        })
        lease_b = self.env['agri.robotics.lease'].create({
            'res_model': 'farm.location',
            'res_id': self.location.id,
            'robot_id': self.robot_b.id,
            'expiration_date': now + timedelta(hours=1),
            'state': 'queued'
        })

        # Release lease_a
        lease_a.action_release()
        self.assertEqual(lease_a.state, 'released', "Lease A must be released")
        self.assertEqual(lease_b.state, 'active', "Lease B must be automatically advanced to 'active'")

    def test_03_mission_auto_release_linkage(self):
        """ Mission completed/failed status must trigger automatic lease release """
        now = fields.Datetime.now()
        mission = self.env['farm.robot.mission'].create({
            'name': 'Test Drone Mission',
            'robot_id': self.robot_a.id,
            'state': 'in_progress'
        })
        
        lease = self.env['agri.robotics.lease'].create({
            'res_model': 'farm.location',
            'res_id': self.location.id,
            'robot_id': self.robot_a.id,
            'mission_id': mission.id,
            'expiration_date': now + timedelta(hours=2),
            'state': 'active'
        })

        # Complete mission
        mission.write({'state': 'completed'})
        self.assertEqual(lease.state, 'released', "Completed mission must automatically release active lease")

    def test_04_hard_expiry_scheduler_cron(self):
        """ Scheduler cron must mark old leases expired and wake up queue """
        now = fields.Datetime.now()
        lease_a = self.env['agri.robotics.lease'].create({
            'res_model': 'farm.location',
            'res_id': self.location.id,
            'robot_id': self.robot_a.id,
            'expiration_date': now - timedelta(minutes=5), # expired
            'state': 'active'
        })
        lease_b = self.env['agri.robotics.lease'].create({
            'res_model': 'farm.location',
            'res_id': self.location.id,
            'robot_id': self.robot_b.id,
            'expiration_date': now + timedelta(hours=1),
            'state': 'queued'
        })

        # Run scheduler
        self.env['agri.robotics.lease']._cron_check_expired_leases()
        self.assertEqual(lease_a.state, 'expired', "Lease A must be marked as expired")
        self.assertEqual(lease_b.state, 'active', "Lease B must be advanced to active status")
