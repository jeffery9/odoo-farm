from odoo import models, fields, api, _
import time
import logging
from datetime import datetime

_logger = logging.getLogger(__name__)


class AgriPerformanceMonitor(models.Model):
    """
    Performance monitoring for agricultural operations
    """
    _name = 'agri.performance.monitor'
    _description = 'Agricultural Performance Monitor'
    _order = 'start_time desc'

    name = fields.Char(string="Operation Name", required=True)
    model_name = fields.Char(string="Model Name", required=True)
    operation = fields.Char(string="Operation Type", required=True)
    start_time = fields.Datetime(string="Start Time", default=fields.Datetime.now)
    end_time = fields.Datetime(string="End Time")
    duration = fields.Float(string="Duration (seconds)", compute='_compute_duration', store=True)
    record_count = fields.Integer(string="Record Count", default=1)
    cpu_time = fields.Float(string="CPU Time (seconds)")
    peak_memory_mb = fields.Float(string="Peak Memory (MB)")
    status = fields.Selection([
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ], default='running')
    details = fields.Text(string="Details")
    user_id = fields.Many2one('res.users', string="User", default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)

    @api.depends('start_time', 'end_time')
    def _compute_duration(self):
        for record in self:
            if record.start_time and record.end_time:
                start = fields.Datetime.from_string(record.start_time)
                end = fields.Datetime.from_string(record.end_time)
                record.duration = (end - start).total_seconds()
            else:
                record.duration = 0.0

    @api.model
    def start_monitoring(self, operation_name, model_name, operation_type, record_count=1, details=None):
        """
        Start performance monitoring for an operation
        """
        return self.create({
            'name': operation_name,
            'model_name': model_name,
            'operation': operation_type,
            'record_count': record_count,
            'details': details or f"Started {operation_type} on {model_name}",
            'status': 'running'
        })

    def stop_monitoring(self, status='completed', details=None):
        """
        Stop performance monitoring for an operation
        """
        for record in self:
            record.end_time = fields.Datetime.now()
            record.status = status
            if details:
                if record.details:
                    record.details += f"\n{details}"
                else:
                    record.details = details

    def check_performance_thresholds(self, max_duration=5.0):
        """
        Check if monitored operations exceeded performance thresholds
        """
        slow_operations = self.search([
            ('duration', '>', max_duration),
            ('status', '=', 'completed')
        ])

        if slow_operations:
            slow_details = []
            for op in slow_operations:
                slow_details.append(f"{op.operation} on {op.model_name}: {op.duration:.2f}s")

            _logger.warning(f"Slow operations detected: {', '.join(slow_details)}")

        return slow_operations

    def cleanup_old_records(self, days=30):
        """
        Clean up old performance monitoring records
        """
        cutoff_date = fields.Datetime.to_string(
            fields.Datetime.now() - datetime.timedelta(days=days)
        )

        old_records = self.search([('start_time', '<', cutoff_date)])
        old_count = len(old_records)
        old_records.unlink()

        _logger.info(f"Cleaned up {old_count} old performance monitoring records")

        return {'deleted': old_count}


class PerformanceMonitoringMixin(models.AbstractModel):
    """
    Mixin to add performance monitoring to any model
    """
    _name = 'agri.performance.monitoring.mixin'
    _description = 'Agricultural Performance Monitoring Mixin'

    performance_monitor_ids = fields.One2many(
        'agri.performance.monitor',
        'model_name',
        string="Performance Monitors",
        compute='_compute_performance_monitors'
    )

    def _compute_performance_monitors(self):
        """Compute the related performance monitors"""
        for record in self:
            record.performance_monitor_ids = self.env['agri.performance.monitor'].search([
                ('model_name', '=', self._name)
            ], limit=10)  # Limit to last 10 monitors

    def _with_performance_monitoring(self, operation_name, operation_func, *args, **kwargs):
        """
        Execute a function with performance monitoring
        """
        monitor = self.env['agri.performance.monitor'].start_monitoring(
            operation_name,
            self._name,
            operation_func.__name__,
            record_count=len(self)
        )

        start_time = time.time()
        try:
            result = operation_func(self, *args, **kwargs)
            monitor.stop_monitoring(status='completed')
            return result
        except Exception as e:
            monitor.stop_monitoring(status='failed', details=str(e))
            raise e
        finally:
            actual_duration = time.time() - start_time
            # Update duration directly since it might not be computed yet
            if monitor.duration == 0:
                monitor.end_time = fields.Datetime.now()
                monitor.duration = actual_duration