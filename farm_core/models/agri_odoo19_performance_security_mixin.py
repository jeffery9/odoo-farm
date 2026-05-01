from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessError, UserError
import logging
import json
import time
from datetime import datetime

_logger = logging.getLogger(__name__)


class AgriOdoo19PerformanceSecurityMixin(models.AbstractModel):
    """
    Mixin for Odoo 19 Performance and Security Enhancements
    Level 4: Performance, Security and Odoo 19 Features Integration
    """
    _name = 'agri.odoo19.performance.security.mixin'
    _description = 'Agricultural Odoo 19 Performance and Security Mixin'

    # JSON field for flexible configuration storage
    config_settings = fields.Json(
        string="Configuration Settings",
        default=dict,
        help="Flexible JSON storage for configuration parameters, performance thresholds and security settings"
    )

    # Performance tracking fields
    performance_metrics = fields.Json(
        string="Performance Metrics",
        default=dict,
        help="Runtime performance metrics and statistics"
    )

    # Security and audit fields
    security_level = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ], string="Security Level", default='medium', required=True)

    access_log = fields.Json(
        string="Access Log",
        default=list,
        help="Log of access attempts and operations for security auditing"
    )

    # Industry-specific access control
    industry_access_control = fields.Json(
        string="Industry Access Control",
        default=dict,
        help="JSON-based access control rules for different industry types"
    )

    def _default_config_settings(self):
        """Default configuration settings for performance and security"""
        return {
            'performance_thresholds': {
                'max_query_time': 5.0,  # seconds
                'max_record_count': 10000,
                'cache_ttl': 300  # seconds
            },
            'security_settings': {
                'audit_enabled': True,
                'access_logging': True,
                'session_timeout': 3600  # seconds
            },
            'optimization_settings': {
                'batch_operations': True,
                'precompute_enabled': True,
                'caching_enabled': True
            }
        }

    @api.model_create_multi
    def create(self, vals_list):
        """
        Enhanced create method with performance and security checks
        """
        # Apply default config settings if not provided
        for vals in vals_list:
            if 'config_settings' not in vals:
                vals['config_settings'] = self._default_config_settings()

        # Performance: Log creation time
        start_time = time.time()

        # Security: Check permissions before creating
        self._check_security_permissions('create')

        # Call parent create method
        records = super().create(vals_list)

        # Performance: Log metrics
        duration = time.time() - start_time
        if duration > records[0].config_settings.get('performance_thresholds', {}).get('max_query_time', 5.0):
            _logger.warning(f"Slow CREATE operation on {self._name}: {duration:.2f}s for {len(records)} records")

        # Security: Log access
        records._log_access('create')

        return records

    def write(self, vals):
        """
        Enhanced write method with performance and security checks
        """
        # Performance: Log execution time
        start_time = time.time()

        # Security: Check permissions before writing
        self._check_security_permissions('write')

        # Call parent write method
        result = super().write(vals)

        # Performance: Log metrics if operation was slow
        duration = time.time() - start_time
        max_time = self.config_settings[0].get('performance_thresholds', {}).get('max_query_time', 5.0) if self else 5.0
        if duration > max_time:
            _logger.warning(f"Slow WRITE operation on {self._name}: {duration:.2f}s for {len(self)} records")

        # Security: Log access
        self._log_access('write')

        return result

    def unlink(self):
        """
        Enhanced unlink method with security checks
        """
        # Security: Check permissions before unlinking
        self._check_security_permissions('unlink')

        # Security: Log access before deletion
        self._log_access('unlink')

        # Call parent unlink method
        return super().unlink()

    def _check_security_permissions(self, operation):
        """
        Enhanced security permission checking with industry-specific rules
        """
        # Check basic Odoo permissions
        if operation == 'create':
            if not self.env.user.has_group('farm_core.group_farm_user'):
                raise AccessError(_("You don't have permission to create records."))
        elif operation == 'write':
            if not self.env.user.has_group('farm_core.group_farm_user'):
                raise AccessError(_("You don't have permission to modify records."))
        elif operation == 'unlink':
            if not self.env.user.has_group('farm_core.group_farm_manager'):
                raise AccessError(_("You don't have permission to delete records."))

        # Industry-specific access control
        for record in self:
            if hasattr(record, 'industry_type') and record.industry_type:
                access_rules = record.industry_access_control or {}
                allowed_groups = access_rules.get(record.industry_type, {}).get(f'{operation}_groups', [])

                if allowed_groups:
                    user_groups = [group.name for group in self.env.user.groups_id]
                    if not any(group in user_groups for group in allowed_groups):
                        raise AccessError(
                            _("You don't have permission to perform '%s' operation on %s industry records.") %
                            (operation, record.industry_type)
                        )

    def _log_access(self, operation):
        """
        Log access for security auditing
        """
        if not self:
            return

        config = self[0].config_settings or self._default_config_settings()
        if not config.get('security_settings', {}).get('access_logging', True):
            return

        for record in self:
            access_log = record.access_log or []
            access_entry = {
                'timestamp': fields.Datetime.now().isoformat(),
                'user_id': self.env.user.id,
                'user_name': self.env.user.name,
                'operation': operation,
                'model': self._name,
                'record_id': record.id,
                'ip_address': self._get_client_ip(),
                'session_id': self.env.context.get('session_id')
            }
            access_log.append(access_entry)

            # Keep only last 1000 log entries
            if len(access_log) > 1000:
                access_log = access_log[-1000:]

            record.access_log = access_log

    def _get_client_ip(self):
        """Get client IP for audit purposes"""
        return (
            self.env.context.get('HTTP_X_FORWARDED_FOR') or
            self.env.context.get('REMOTE_ADDR') or
            '127.0.0.1'
        )

    def _check_performance_thresholds(self, operation, duration, record_count=1):
        """
        Check if operation exceeded performance thresholds
        """
        config = self._default_config_settings() if not self else (self[0].config_settings or self._default_config_settings())
        thresholds = config.get('performance_thresholds', {})

        max_time = thresholds.get('max_query_time', 5.0)
        max_records = thresholds.get('max_record_count', 10000)

        if duration > max_time:
            _logger.warning(
                f"Performance threshold exceeded: {operation} on {self._name} took {duration:.2f}s "
                f"(threshold: {max_time}s) for {record_count} records"
            )
            return False

        if record_count > max_records:
            _logger.warning(
                f"Record count threshold exceeded: {operation} on {self._name} "
                f"affected {record_count} records (threshold: {max_records})"
            )
            return False

        return True

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        """
        Enhanced search with performance tracking
        """
        start_time = time.time()
        result = super().search(args, offset=offset, limit=limit, order=order, count=count)

        duration = time.time() - start_time
        record_count = result if count else len(result) if isinstance(result, models.Model) else 0

        # Check performance thresholds
        self._check_performance_thresholds('search', duration, record_count)

        return result

    def _compute_performance_optimized(self, field_name, compute_func, recordset=None):
        """
        Generic optimized compute method with caching and precompute support
        """
        records = recordset or self
        config = records[0].config_settings if records else self._default_config_settings()
        is_precompute_enabled = config.get('optimization_settings', {}).get('precompute_enabled', True)

        # If precompute is enabled, compute immediately
        if is_precompute_enabled:
            for record in records:
                compute_func(record)
        else:
            # Batch compute for better performance
            compute_func(records)


class AgriBatchOperationMixin(models.AbstractModel):
    """
    Mixin for batch operations to improve performance
    Level 3: Batch Processing Performance Enhancement
    """
    _name = 'agri.batch.operation.mixin'
    _description = 'Agricultural Batch Operation Mixin'

    def batch_operation(self, operation_func, batch_size=1000, *args, **kwargs):
        """
        Generic batch operation function to handle large datasets efficiently
        """
        total_records = len(self)
        processed = 0
        errors = 0

        _logger.info(f"Starting batch operation on {total_records} records with batch size {batch_size}")

        for i in range(0, total_records, batch_size):
            batch = self[i:i + batch_size]

            try:
                # Execute the operation on the batch
                operation_func(batch, *args, **kwargs)
                processed += len(batch)

                # Commit every batch to avoid memory issues
                self.env.cr.commit()

            except Exception as e:
                errors += len(batch)
                _logger.error(f"Batch operation failed for batch starting at {i}: {str(e)}")

                # Log the error for later analysis
                self.env['agri.audit.log'].sudo().create({
                    'model_name': self._name,
                    'operation': 'batch_operation',
                    'user_id': self.env.user.id,
                    'timestamp': fields.Datetime.now(),
                    'details': f"Batch operation failed: {str(e)} on records {i} to {min(i + batch_size, total_records)}",
                    'severity': 'error'
                })

        _logger.info(f"Batch operation completed: {processed} processed, {errors} errors")

        return {
            'total': total_records,
            'processed': processed,
            'errors': errors,
            'success_rate': (processed - errors) / total_records if total_records > 0 else 0
        }

    def batch_update(self, vals, batch_size=1000):
        """
        Batch update operation for better performance
        """
        def update_batch(batch, update_vals):
            batch.write(update_vals)

        return self.batch_operation(update_batch, batch_size, vals)


class AgriAuditLog(models.Model):
    """
    Audit log model for tracking security and performance events
    """
    _name = 'agri.audit.log'
    _description = 'Agricultural Audit Log'
    _order = 'timestamp desc'

    model_name = fields.Char(string="Model Name", required=True)
    record_id = fields.Integer(string="Record ID")
    operation = fields.Char(string="Operation", required=True)
    user_id = fields.Many2one('res.users', string="User")
    timestamp = fields.Datetime(string="Timestamp", required=True, default=fields.Datetime.now)
    details = fields.Text(string="Details")
    severity = fields.Selection([
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('critical', 'Critical')
    ], default='info')
    ip_address = fields.Char(string="IP Address")
    session_id = fields.Char(string="Session ID")

    def cleanup_old_logs(self, days=30):
        """
        Clean up audit logs older than specified days
        """
        cutoff_date = fields.Datetime.to_string(
            fields.Datetime.now() - datetime.timedelta(days=days)
        )

        old_logs = self.search([('timestamp', '<', cutoff_date)])
        old_logs_count = len(old_logs)
        old_logs.unlink()

        _logger.info(f"Cleaned up {old_logs_count} audit logs older than {days} days")

        return {'deleted': old_logs_count}