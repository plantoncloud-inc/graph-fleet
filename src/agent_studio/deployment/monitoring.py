"""Agent Deployment Monitoring System

Provides comprehensive monitoring capabilities for deployed agents including
health checks, performance metrics, error tracking, and alerting.
"""

import asyncio
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime, timezone, timedelta
from enum import Enum
from pydantic import BaseModel, Field
import logging
import aiohttp
import psutil

logger = logging.getLogger(__name__)


class DeploymentStatus(str, Enum):
    """Deployment status values"""
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"
    STARTING = "starting"
    STOPPING = "stopping"


class MetricType(str, Enum):
    """Types of metrics collected"""
    RESPONSE_TIME = "response_time"
    REQUEST_COUNT = "request_count"
    ERROR_RATE = "error_rate"
    CPU_USAGE = "cpu_usage"
    MEMORY_USAGE = "memory_usage"
    DISK_USAGE = "disk_usage"
    NETWORK_IO = "network_io"


class AlertSeverity(str, Enum):
    """Alert severity levels"""
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"


class HealthCheck(BaseModel):
    """Health check configuration and result"""
    
    endpoint: str = Field(..., description="Health check endpoint URL")
    method: str = Field("GET", description="HTTP method")
    timeout: int = Field(30, description="Timeout in seconds")
    expected_status: int = Field(200, description="Expected HTTP status code")
    expected_response: Optional[str] = Field(None, description="Expected response content")
    
    # Check results
    last_check: Optional[datetime] = Field(None, description="Last check timestamp")
    status: DeploymentStatus = Field(DeploymentStatus.UNKNOWN, description="Current status")
    response_time: Optional[float] = Field(None, description="Last response time in seconds")
    error_message: Optional[str] = Field(None, description="Last error message")
    consecutive_failures: int = Field(0, description="Number of consecutive failures")
    
    class Config:
        use_enum_values = True


class Metric(BaseModel):
    """Performance metric data point"""
    
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metric_type: MetricType = Field(..., description="Type of metric")
    value: float = Field(..., description="Metric value")
    unit: str = Field("", description="Unit of measurement")
    labels: Dict[str, str] = Field(default_factory=dict, description="Metric labels")
    
    class Config:
        use_enum_values = True


class Alert(BaseModel):
    """Alert configuration and state"""
    
    id: str = Field(..., description="Alert ID")
    name: str = Field(..., description="Alert name")
    description: str = Field("", description="Alert description")
    
    # Alert conditions
    metric_type: MetricType = Field(..., description="Metric to monitor")
    threshold: float = Field(..., description="Alert threshold")
    comparison: str = Field("greater_than", description="Comparison operator")
    duration: int = Field(300, description="Duration in seconds before alerting")
    
    # Alert state
    severity: AlertSeverity = Field(AlertSeverity.WARNING, description="Alert severity")
    is_active: bool = Field(False, description="Whether alert is currently active")
    triggered_at: Optional[datetime] = Field(None, description="When alert was triggered")
    resolved_at: Optional[datetime] = Field(None, description="When alert was resolved")
    
    # Notification settings
    notify_channels: List[str] = Field(default_factory=list, description="Notification channels")
    
    class Config:
        use_enum_values = True


class DeploymentMonitor(BaseModel):
    """Monitor configuration for a deployment"""
    
    deployment_id: str = Field(..., description="Deployment ID")
    agent_id: str = Field(..., description="Agent ID")
    
    # Health check configuration
    health_checks: List[HealthCheck] = Field(default_factory=list, description="Health checks")
    check_interval: int = Field(60, description="Health check interval in seconds")
    
    # Metrics collection
    collect_metrics: bool = Field(True, description="Whether to collect metrics")
    metrics_interval: int = Field(30, description="Metrics collection interval in seconds")
    
    # Alerting
    alerts: List[Alert] = Field(default_factory=list, description="Alert configurations")
    
    # Monitoring state
    is_monitoring: bool = Field(False, description="Whether monitoring is active")
    started_at: Optional[datetime] = Field(None, description="When monitoring started")
    last_check: Optional[datetime] = Field(None, description="Last health check")
    
    # Collected data
    metrics: List[Metric] = Field(default_factory=list, description="Collected metrics")
    status_history: List[Dict[str, Any]] = Field(default_factory=list, description="Status change history")


class MonitoringManager:
    """Manages monitoring for deployed agents"""
    
    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or self._find_project_root()
        self.monitoring_dir = self.project_root / "monitoring"
        self.monitoring_dir.mkdir(exist_ok=True)
        
        # Active monitors
        self.monitors: Dict[str, DeploymentMonitor] = {}
        self.monitoring_tasks: Dict[str, asyncio.Task] = {}
        
        # Notification handlers
        self.notification_handlers: Dict[str, Callable] = {}
        
        # Load existing monitors
        self._load_monitors()
    
    def _find_project_root(self) -> Path:
        """Find the project root directory"""
        current = Path(__file__).resolve()
        for parent in current.parents:
            if (parent / "pyproject.toml").exists() or (parent / "langgraph.json").exists():
                return parent
        return Path.cwd()
    
    def _load_monitors(self):
        """Load existing monitors from disk"""
        monitors_file = self.monitoring_dir / "monitors.json"
        if monitors_file.exists():
            try:
                with open(monitors_file, 'r') as f:
                    data = json.load(f)
                    for deployment_id, monitor_data in data.items():
                        self.monitors[deployment_id] = DeploymentMonitor(**monitor_data)
            except Exception as e:
                logger.error(f"Failed to load monitors: {e}")
    
    def _save_monitors(self):
        """Save monitors to disk"""
        monitors_file = self.monitoring_dir / "monitors.json"
        try:
            data = {
                deployment_id: monitor.dict()
                for deployment_id, monitor in self.monitors.items()
            }
            with open(monitors_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save monitors: {e}")
    
    def create_monitor(self, deployment_id: str, agent_id: str, 
                      health_check_url: Optional[str] = None,
                      check_interval: int = 60,
                      metrics_interval: int = 30) -> DeploymentMonitor:
        """Create a new deployment monitor"""
        
        monitor = DeploymentMonitor(
            deployment_id=deployment_id,
            agent_id=agent_id,
            check_interval=check_interval,
            metrics_interval=metrics_interval
        )
        
        # Add default health check if URL provided
        if health_check_url:
            health_check = HealthCheck(endpoint=health_check_url)
            monitor.health_checks.append(health_check)
        
        # Add default alerts
        default_alerts = self._create_default_alerts(deployment_id)
        monitor.alerts.extend(default_alerts)
        
        self.monitors[deployment_id] = monitor
        self._save_monitors()
        
        logger.info(f"Created monitor for deployment {deployment_id}")
        return monitor
    
    def _create_default_alerts(self, deployment_id: str) -> List[Alert]:
        """Create default alert configurations"""
        return [
            Alert(
                id=f"{deployment_id}-response-time",
                name="High Response Time",
                description="Response time is above threshold",
                metric_type=MetricType.RESPONSE_TIME,
                threshold=5.0,
                comparison="greater_than",
                severity=AlertSeverity.WARNING
            ),
            Alert(
                id=f"{deployment_id}-error-rate",
                name="High Error Rate",
                description="Error rate is above threshold",
                metric_type=MetricType.ERROR_RATE,
                threshold=0.05,  # 5%
                comparison="greater_than",
                severity=AlertSeverity.CRITICAL
            ),
            Alert(
                id=f"{deployment_id}-cpu-usage",
                name="High CPU Usage",
                description="CPU usage is above threshold",
                metric_type=MetricType.CPU_USAGE,
                threshold=80.0,
                comparison="greater_than",
                severity=AlertSeverity.WARNING
            ),
            Alert(
                id=f"{deployment_id}-memory-usage",
                name="High Memory Usage",
                description="Memory usage is above threshold",
                metric_type=MetricType.MEMORY_USAGE,
                threshold=85.0,
                comparison="greater_than",
                severity=AlertSeverity.WARNING
            )
        ]
    
    async def start_monitoring(self, deployment_id: str) -> bool:
        """Start monitoring a deployment"""
        monitor = self.monitors.get(deployment_id)
        if not monitor:
            logger.error(f"Monitor not found for deployment {deployment_id}")
            return False
        
        if monitor.is_monitoring:
            logger.info(f"Monitoring already active for deployment {deployment_id}")
            return True
        
        # Start monitoring task
        task = asyncio.create_task(self._monitoring_loop(deployment_id))
        self.monitoring_tasks[deployment_id] = task
        
        monitor.is_monitoring = True
        monitor.started_at = datetime.now(timezone.utc)
        self._save_monitors()
        
        logger.info(f"Started monitoring for deployment {deployment_id}")
        return True
    
    async def stop_monitoring(self, deployment_id: str) -> bool:
        """Stop monitoring a deployment"""
        monitor = self.monitors.get(deployment_id)
        if not monitor:
            return False
        
        # Cancel monitoring task
        if deployment_id in self.monitoring_tasks:
            self.monitoring_tasks[deployment_id].cancel()
            del self.monitoring_tasks[deployment_id]
        
        monitor.is_monitoring = False
        self._save_monitors()
        
        logger.info(f"Stopped monitoring for deployment {deployment_id}")
        return True
    
    async def _monitoring_loop(self, deployment_id: str):
        """Main monitoring loop for a deployment"""
        monitor = self.monitors[deployment_id]
        
        try:
            while monitor.is_monitoring:
                # Perform health checks
                await self._perform_health_checks(monitor)
                
                # Collect metrics
                if monitor.collect_metrics:
                    await self._collect_metrics(monitor)
                
                # Check alerts
                await self._check_alerts(monitor)
                
                # Update last check time
                monitor.last_check = datetime.now(timezone.utc)
                self._save_monitors()
                
                # Wait for next check
                await asyncio.sleep(min(monitor.check_interval, monitor.metrics_interval))
                
        except asyncio.CancelledError:
            logger.info(f"Monitoring cancelled for deployment {deployment_id}")
        except Exception as e:
            logger.error(f"Monitoring error for deployment {deployment_id}: {e}")
    
    async def _perform_health_checks(self, monitor: DeploymentMonitor):
        """Perform health checks for a deployment"""
        for health_check in monitor.health_checks:
            try:
                start_time = time.time()
                
                async with aiohttp.ClientSession() as session:
                    async with session.request(
                        health_check.method,
                        health_check.endpoint,
                        timeout=aiohttp.ClientTimeout(total=health_check.timeout)
                    ) as response:
                        response_time = time.time() - start_time
                        
                        # Check status code
                        if response.status == health_check.expected_status:
                            # Check response content if specified
                            if health_check.expected_response:
                                content = await response.text()
                                if health_check.expected_response not in content:
                                    raise ValueError(f"Unexpected response content")
                            
                            # Health check passed
                            old_status = health_check.status
                            health_check.status = DeploymentStatus.HEALTHY
                            health_check.response_time = response_time
                            health_check.error_message = None
                            health_check.consecutive_failures = 0
                            
                            # Log status change
                            if old_status != DeploymentStatus.HEALTHY:
                                self._log_status_change(monitor, old_status, DeploymentStatus.HEALTHY)
                            
                        else:
                            raise ValueError(f"Unexpected status code: {response.status}")
                        
            except Exception as e:
                # Health check failed
                old_status = health_check.status
                health_check.status = DeploymentStatus.UNHEALTHY
                health_check.error_message = str(e)
                health_check.consecutive_failures += 1
                
                # Log status change
                if old_status != DeploymentStatus.UNHEALTHY:
                    self._log_status_change(monitor, old_status, DeploymentStatus.UNHEALTHY)
                
                logger.warning(f"Health check failed for {health_check.endpoint}: {e}")
            
            finally:
                health_check.last_check = datetime.now(timezone.utc)
    
    async def _collect_metrics(self, monitor: DeploymentMonitor):
        """Collect performance metrics for a deployment"""
        timestamp = datetime.now(timezone.utc)
        
        try:
            # Collect system metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Add CPU metric
            monitor.metrics.append(Metric(
                timestamp=timestamp,
                metric_type=MetricType.CPU_USAGE,
                value=cpu_percent,
                unit="percent"
            ))
            
            # Add memory metric
            monitor.metrics.append(Metric(
                timestamp=timestamp,
                metric_type=MetricType.MEMORY_USAGE,
                value=memory.percent,
                unit="percent"
            ))
            
            # Add disk metric
            monitor.metrics.append(Metric(
                timestamp=timestamp,
                metric_type=MetricType.DISK_USAGE,
                value=disk.percent,
                unit="percent"
            ))
            
            # Collect response time metrics from health checks
            for health_check in monitor.health_checks:
                if health_check.response_time is not None:
                    monitor.metrics.append(Metric(
                        timestamp=timestamp,
                        metric_type=MetricType.RESPONSE_TIME,
                        value=health_check.response_time,
                        unit="seconds",
                        labels={"endpoint": health_check.endpoint}
                    ))
            
            # Keep only recent metrics (last 24 hours)
            cutoff_time = timestamp - timedelta(hours=24)
            monitor.metrics = [
                m for m in monitor.metrics 
                if m.timestamp > cutoff_time
            ]
            
        except Exception as e:
            logger.error(f"Failed to collect metrics for {monitor.deployment_id}: {e}")
    
    async def _check_alerts(self, monitor: DeploymentMonitor):
        """Check alert conditions and trigger notifications"""
        for alert in monitor.alerts:
            try:
                # Get recent metrics for this alert type
                recent_metrics = [
                    m for m in monitor.metrics
                    if m.metric_type == alert.metric_type
                    and m.timestamp > datetime.now(timezone.utc) - timedelta(seconds=alert.duration)
                ]
                
                if not recent_metrics:
                    continue
                
                # Calculate average value over the duration
                avg_value = sum(m.value for m in recent_metrics) / len(recent_metrics)
                
                # Check threshold
                should_trigger = False
                if alert.comparison == "greater_than":
                    should_trigger = avg_value > alert.threshold
                elif alert.comparison == "less_than":
                    should_trigger = avg_value < alert.threshold
                elif alert.comparison == "equals":
                    should_trigger = abs(avg_value - alert.threshold) < 0.001
                
                # Handle alert state changes
                if should_trigger and not alert.is_active:
                    # Trigger alert
                    alert.is_active = True
                    alert.triggered_at = datetime.now(timezone.utc)
                    alert.resolved_at = None
                    
                    await self._send_alert_notification(monitor, alert, avg_value)
                    logger.warning(f"Alert triggered: {alert.name} for deployment {monitor.deployment_id}")
                
                elif not should_trigger and alert.is_active:
                    # Resolve alert
                    alert.is_active = False
                    alert.resolved_at = datetime.now(timezone.utc)
                    
                    await self._send_alert_resolution(monitor, alert)
                    logger.info(f"Alert resolved: {alert.name} for deployment {monitor.deployment_id}")
                
            except Exception as e:
                logger.error(f"Failed to check alert {alert.name}: {e}")
    
    def _log_status_change(self, monitor: DeploymentMonitor, 
                          old_status: DeploymentStatus, 
                          new_status: DeploymentStatus):
        """Log a status change"""
        status_change = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "from_status": old_status,
            "to_status": new_status
        }
        
        monitor.status_history.append(status_change)
        
        # Keep only recent history (last 100 changes)
        if len(monitor.status_history) > 100:
            monitor.status_history = monitor.status_history[-100:]
        
        logger.info(f"Status change for {monitor.deployment_id}: {old_status} -> {new_status}")
    
    async def _send_alert_notification(self, monitor: DeploymentMonitor, 
                                     alert: Alert, current_value: float):
        """Send alert notification"""
        message = f"""
Alert: {alert.name}
Deployment: {monitor.deployment_id}
Agent: {monitor.agent_id}
Severity: {alert.severity}
Current Value: {current_value}
Threshold: {alert.threshold}
Description: {alert.description}
"""
        
        # Send to configured notification channels
        for channel in alert.notify_channels:
            if channel in self.notification_handlers:
                try:
                    await self.notification_handlers[channel](message, alert.severity)
                except Exception as e:
                    logger.error(f"Failed to send notification to {channel}: {e}")
    
    async def _send_alert_resolution(self, monitor: DeploymentMonitor, alert: Alert):
        """Send alert resolution notification"""
        message = f"""
Alert Resolved: {alert.name}
Deployment: {monitor.deployment_id}
Agent: {monitor.agent_id}
Resolved at: {alert.resolved_at}
"""
        
        # Send to configured notification channels
        for channel in alert.notify_channels:
            if channel in self.notification_handlers:
                try:
                    await self.notification_handlers[channel](message, AlertSeverity.INFO)
                except Exception as e:
                    logger.error(f"Failed to send resolution notification to {channel}: {e}")
    
    def register_notification_handler(self, channel: str, handler: Callable):
        """Register a notification handler for a channel"""
        self.notification_handlers[channel] = handler
        logger.info(f"Registered notification handler for channel: {channel}")
    
    def get_monitor(self, deployment_id: str) -> Optional[DeploymentMonitor]:
        """Get monitor for a deployment"""
        return self.monitors.get(deployment_id)
    
    def list_monitors(self) -> List[DeploymentMonitor]:
        """List all monitors"""
        return list(self.monitors.values())
    
    def get_deployment_status(self, deployment_id: str) -> DeploymentStatus:
        """Get current status of a deployment"""
        monitor = self.monitors.get(deployment_id)
        if not monitor or not monitor.health_checks:
            return DeploymentStatus.UNKNOWN
        
        # Determine overall status from health checks
        statuses = [hc.status for hc in monitor.health_checks]
        
        if all(s == DeploymentStatus.HEALTHY for s in statuses):
            return DeploymentStatus.HEALTHY
        elif any(s == DeploymentStatus.UNHEALTHY for s in statuses):
            return DeploymentStatus.UNHEALTHY
        else:
            return DeploymentStatus.DEGRADED
    
    def get_metrics(self, deployment_id: str, 
                   metric_type: Optional[MetricType] = None,
                   hours: int = 24) -> List[Metric]:
        """Get metrics for a deployment"""
        monitor = self.monitors.get(deployment_id)
        if not monitor:
            return []
        
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        metrics = [m for m in monitor.metrics if m.timestamp > cutoff_time]
        
        if metric_type:
            metrics = [m for m in metrics if m.metric_type == metric_type]
        
        return sorted(metrics, key=lambda m: m.timestamp)
    
    def get_active_alerts(self, deployment_id: Optional[str] = None) -> List[Alert]:
        """Get active alerts"""
        active_alerts = []
        
        monitors = [self.monitors[deployment_id]] if deployment_id else self.monitors.values()
        
        for monitor in monitors:
            active_alerts.extend([a for a in monitor.alerts if a.is_active])
        
        return active_alerts
    
    def cleanup_old_data(self, days: int = 7):
        """Clean up old monitoring data"""
        cutoff_time = datetime.now(timezone.utc) - timedelta(days=days)
        
        for monitor in self.monitors.values():
            # Clean up old metrics
            monitor.metrics = [
                m for m in monitor.metrics 
                if m.timestamp > cutoff_time
            ]
            
            # Clean up old status history
            monitor.status_history = [
                s for s in monitor.status_history
                if datetime.fromisoformat(s["timestamp"].replace('Z', '+00:00')) > cutoff_time
            ]
        
        self._save_monitors()
        logger.info(f"Cleaned up monitoring data older than {days} days")
