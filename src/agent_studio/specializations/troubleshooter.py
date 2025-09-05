"""Troubleshooter Specialization

This module defines a specialization profile for cloud troubleshooting,
providing expertise in diagnosing and resolving issues across multiple 
cloud providers and services.
"""

from typing import Dict, Any, List
from deepagents import SubAgent
from ..base import SpecializationProfile, CloudProvider


TROUBLESHOOTER_INSTRUCTIONS = """
You are a Cloud Troubleshooting Specialist with deep expertise in diagnosing
and resolving complex issues across AWS, GCP, and Azure cloud platforms.

## Core Responsibilities:

### 1. Issue Diagnosis & Root Cause Analysis
- Systematically diagnose cloud service failures and performance issues
- Perform root cause analysis using logs, metrics, and traces
- Identify cascading failures and dependency issues
- Analyze error patterns and failure modes
- Correlate issues across multiple services and components

### 2. Performance Troubleshooting
- Diagnose application and infrastructure performance problems
- Analyze resource utilization and bottlenecks
- Investigate latency, throughput, and availability issues
- Optimize database and storage performance
- Troubleshoot network connectivity and routing problems

### 3. Service-Specific Troubleshooting
- Container orchestration issues (ECS, GKE, AKS)
- Serverless function problems (Lambda, Cloud Functions, Azure Functions)
- Database connectivity and performance issues
- Load balancer and traffic routing problems
- Storage access and performance issues

### 4. Infrastructure Troubleshooting
- Virtual machine and compute instance issues
- Network configuration and connectivity problems
- Security group and firewall rule conflicts
- DNS resolution and routing issues
- Auto-scaling and capacity management problems

### 5. Application & Integration Issues
- API gateway and service mesh problems
- Message queue and event streaming issues
- CI/CD pipeline failures and deployment problems
- Monitoring and alerting configuration issues
- Third-party integration and webhook problems

### 6. Incident Response & Resolution
- Rapid incident triage and prioritization
- Coordinated troubleshooting across teams
- Escalation procedures and communication
- Post-incident analysis and improvement recommendations
- Documentation of solutions and preventive measures

## Cloud-Specific Troubleshooting Expertise:

### AWS Troubleshooting:
- CloudWatch Logs, Metrics, and X-Ray tracing
- ECS/EKS container troubleshooting
- Lambda function debugging and optimization
- RDS and DynamoDB performance issues
- VPC networking and security group problems
- CloudFormation stack failures
- API Gateway and ALB/NLB issues

### GCP Troubleshooting:
- Cloud Logging, Monitoring, and Cloud Trace
- GKE cluster and workload issues
- Cloud Functions debugging
- Cloud SQL and Firestore problems
- VPC networking and firewall rules
- Cloud Build and deployment issues
- Cloud Load Balancing problems

### Azure Troubleshooting:
- Azure Monitor, Log Analytics, and Application Insights
- AKS cluster troubleshooting
- Azure Functions debugging
- Azure SQL and Cosmos DB issues
- Virtual Network and NSG problems
- Azure DevOps pipeline failures
- Application Gateway and Load Balancer issues

## Troubleshooting Methodology:

1. **Initial Assessment**
   - Gather symptoms and error descriptions
   - Identify affected services and components
   - Determine impact scope and severity
   - Collect relevant logs and metrics

2. **Systematic Investigation**
   - Follow structured troubleshooting workflows
   - Use divide-and-conquer approach
   - Test hypotheses with targeted experiments
   - Isolate variables and dependencies

3. **Root Cause Identification**
   - Analyze logs, metrics, and traces
   - Correlate events across time and services
   - Identify configuration changes and deployments
   - Validate root cause with evidence

4. **Solution Implementation**
   - Develop and test remediation steps
   - Implement fixes with minimal risk
   - Validate resolution effectiveness
   - Monitor for regression or side effects

5. **Prevention & Documentation**
   - Document troubleshooting process and solution
   - Identify preventive measures and improvements
   - Update monitoring and alerting
   - Share knowledge with team members

## Troubleshooting Tools & Techniques:
- Log aggregation and analysis platforms
- Application Performance Monitoring (APM) tools
- Distributed tracing systems
- Infrastructure monitoring and metrics
- Network analysis and packet capture
- Load testing and performance profiling
- Configuration management and drift detection

## Common Issue Categories:
- **Connectivity**: Network, DNS, firewall, routing
- **Performance**: Latency, throughput, resource utilization
- **Availability**: Service outages, health checks, failover
- **Configuration**: Misconfigurations, version conflicts, dependencies
- **Capacity**: Resource limits, scaling, quota exhaustion
- **Security**: Access denied, certificate issues, authentication

Always provide systematic, evidence-based troubleshooting approaches with
clear diagnostic steps, solution options, and preventive recommendations.
Focus on both immediate resolution and long-term reliability improvements.
"""


TROUBLESHOOTER_SUB_AGENTS = [
    {
        "name": "log_analyzer",
        "description": "Analyzes logs and traces to identify error patterns and root causes",
        "prompt": """
You are a Log Analysis Specialist focused on extracting insights from cloud service logs.

Focus on:
- Error pattern identification and correlation
- Log parsing and structured analysis
- Timeline reconstruction of events
- Anomaly detection in log patterns
- Cross-service log correlation

For each log analysis:
- Identify key error messages and codes
- Correlate timestamps across services
- Extract relevant context and metadata
- Highlight unusual patterns or anomalies
- Provide actionable insights from log data
"""
    },
    {
        "name": "performance_diagnostician",
        "description": "Diagnoses performance issues and resource bottlenecks",
        "prompt": """
You are a Performance Diagnostician specializing in cloud performance troubleshooting.

Focus on:
- Resource utilization analysis (CPU, memory, disk, network)
- Application performance bottleneck identification
- Database query and connection analysis
- Network latency and throughput issues
- Caching and optimization opportunities

For each performance issue:
- Identify specific bottlenecks and constraints
- Analyze resource utilization patterns
- Recommend performance optimizations
- Suggest monitoring and alerting improvements
- Provide capacity planning insights
"""
    },
    {
        "name": "connectivity_specialist",
        "description": "Troubleshoots network connectivity and routing issues",
        "prompt": """
You are a Network Connectivity Specialist focused on cloud networking troubleshooting.

Focus on:
- Network connectivity and routing problems
- DNS resolution and configuration issues
- Security group and firewall rule analysis
- Load balancer and traffic distribution problems
- VPN and private connectivity issues

For each connectivity issue:
- Trace network paths and routing
- Analyze security group and firewall rules
- Test connectivity at different network layers
- Identify DNS and routing misconfigurations
- Recommend network architecture improvements
"""
    },
    {
        "name": "service_debugger",
        "description": "Debugs cloud service-specific issues and configurations",
        "prompt": """
You are a Cloud Service Debugger specializing in service-specific troubleshooting.

Focus on:
- Container orchestration issues (ECS, GKE, AKS)
- Serverless function debugging and optimization
- Database connectivity and performance problems
- Message queue and event processing issues
- API gateway and service mesh problems

For each service issue:
- Analyze service-specific configurations
- Review health checks and monitoring
- Identify service dependencies and interactions
- Recommend service optimization strategies
- Suggest reliability and resilience improvements
"""
    }
]


def create_troubleshooter_profile() -> SpecializationProfile:
    """Create a troubleshooter specialization profile
    
    Returns:
        SpecializationProfile configured for cloud troubleshooting
    """
    return SpecializationProfile(
        name="troubleshooter",
        display_name="Cloud Troubleshooter",
        description="Specializes in diagnosing and resolving complex cloud issues and performance problems",
        version="1.0.0",
        supported_cloud_providers=[
            CloudProvider.AWS,
            CloudProvider.GCP,
            CloudProvider.AZURE
        ],
        instruction_template=TROUBLESHOOTER_INSTRUCTIONS,
        sub_agent_configs=TROUBLESHOOTER_SUB_AGENTS,
        tool_preferences={
            "logging": ["cloudwatch_logs", "cloud_logging", "log_analytics"],
            "monitoring": ["cloudwatch", "cloud_monitoring", "azure_monitor"],
            "tracing": ["xray", "cloud_trace", "application_insights"],
            "networking": ["vpc_flow_logs", "network_watcher", "cloud_nat"]
        },
        required_permissions=[
            "logs:read",
            "monitoring:read",
            "tracing:read",
            "networking:read",
            "compute:read",
            "storage:read"
        ],
        tags=["troubleshooting", "debugging", "performance", "diagnostics", "incident-response"],
        capabilities=[
            "issue_diagnosis",
            "root_cause_analysis",
            "performance_troubleshooting",
            "connectivity_debugging",
            "log_analysis",
            "incident_response"
        ]
    )


def create_troubleshooter_subagents() -> List[SubAgent]:
    """Create sub-agents for troubleshooter specialization
    
    Returns:
        List of SubAgent instances for troubleshooting tasks
    """
    return [
        SubAgent(
            name=config["name"],
            description=config["description"],
            prompt=config["prompt"]
        )
        for config in TROUBLESHOOTER_SUB_AGENTS
    ]


def get_troubleshooting_workflows() -> Dict[str, List[str]]:
    """Get troubleshooting workflows by issue type
    
    Returns:
        Dictionary of troubleshooting workflows organized by issue category
    """
    return {
        "connectivity_issues": [
            "Verify network connectivity at different layers",
            "Check DNS resolution and routing",
            "Analyze security group and firewall rules",
            "Test load balancer and proxy configurations",
            "Validate SSL/TLS certificates and protocols"
        ],
        "performance_issues": [
            "Collect performance metrics and baselines",
            "Identify resource bottlenecks and constraints",
            "Analyze application and database performance",
            "Review caching and optimization strategies",
            "Test under different load conditions"
        ],
        "service_failures": [
            "Check service health and status",
            "Review recent deployments and changes",
            "Analyze error logs and exception patterns",
            "Validate service dependencies and integrations",
            "Test service recovery and failover mechanisms"
        ],
        "configuration_issues": [
            "Compare current vs expected configurations",
            "Identify configuration drift and changes",
            "Validate environment-specific settings",
            "Check version compatibility and dependencies",
            "Review access permissions and policies"
        ]
    }


def get_diagnostic_commands() -> Dict[str, Dict[str, List[str]]]:
    """Get diagnostic commands by cloud provider and service type
    
    Returns:
        Dictionary of diagnostic commands organized by cloud provider and service
    """
    return {
        "aws": {
            "compute": [
                "aws ec2 describe-instances",
                "aws ecs describe-services",
                "aws lambda get-function",
                "aws autoscaling describe-auto-scaling-groups"
            ],
            "networking": [
                "aws ec2 describe-security-groups",
                "aws ec2 describe-vpc-endpoints",
                "aws elbv2 describe-load-balancers",
                "aws route53 list-resource-record-sets"
            ],
            "monitoring": [
                "aws logs describe-log-groups",
                "aws cloudwatch get-metric-statistics",
                "aws xray get-trace-summaries",
                "aws config describe-configuration-recorders"
            ]
        },
        "gcp": {
            "compute": [
                "gcloud compute instances list",
                "gcloud container clusters list",
                "gcloud functions list",
                "gcloud compute instance-groups list"
            ],
            "networking": [
                "gcloud compute firewall-rules list",
                "gcloud compute networks list",
                "gcloud compute forwarding-rules list",
                "gcloud dns managed-zones list"
            ],
            "monitoring": [
                "gcloud logging logs list",
                "gcloud monitoring metrics list",
                "gcloud trace list-traces",
                "gcloud config list"
            ]
        },
        "azure": {
            "compute": [
                "az vm list",
                "az aks list",
                "az functionapp list",
                "az vmss list"
            ],
            "networking": [
                "az network nsg list",
                "az network vnet list",
                "az network lb list",
                "az network dns zone list"
            ],
            "monitoring": [
                "az monitor log-analytics workspace list",
                "az monitor metrics list",
                "az monitor app-insights component list",
                "az monitor activity-log list"
            ]
        }
    }


def get_common_error_patterns() -> Dict[str, Dict[str, Any]]:
    """Get common error patterns and their solutions
    
    Returns:
        Dictionary of common error patterns with diagnostic and solution information
    """
    return {
        "connection_timeout": {
            "description": "Connection timeout errors",
            "common_causes": [
                "Network connectivity issues",
                "Security group/firewall blocking",
                "Service overload or unavailability",
                "DNS resolution problems"
            ],
            "diagnostic_steps": [
                "Test network connectivity",
                "Check security group rules",
                "Verify service health",
                "Validate DNS resolution"
            ],
            "solutions": [
                "Fix network routing",
                "Update security group rules",
                "Scale service capacity",
                "Configure proper DNS"
            ]
        },
        "permission_denied": {
            "description": "Access denied or permission errors",
            "common_causes": [
                "Insufficient IAM permissions",
                "Expired credentials",
                "Resource policy restrictions",
                "Cross-account access issues"
            ],
            "diagnostic_steps": [
                "Review IAM policies",
                "Check credential validity",
                "Validate resource policies",
                "Test cross-account access"
            ],
            "solutions": [
                "Grant required permissions",
                "Refresh credentials",
                "Update resource policies",
                "Configure trust relationships"
            ]
        },
        "resource_exhaustion": {
            "description": "Resource limit or quota exceeded errors",
            "common_causes": [
                "CPU or memory limits reached",
                "Storage capacity exhausted",
                "Network bandwidth limits",
                "Service quotas exceeded"
            ],
            "diagnostic_steps": [
                "Monitor resource utilization",
                "Check service quotas",
                "Analyze usage patterns",
                "Review scaling policies"
            ],
            "solutions": [
                "Scale resources up/out",
                "Request quota increases",
                "Optimize resource usage",
                "Implement auto-scaling"
            ]
        }
    }


# Export the specialization profile instance
troubleshooter_profile = create_troubleshooter_profile()

__all__ = [
    "TROUBLESHOOTER_INSTRUCTIONS",
    "TROUBLESHOOTER_SUB_AGENTS",
    "create_troubleshooter_profile",
    "create_troubleshooter_subagents",
    "get_troubleshooting_workflows",
    "get_diagnostic_commands",
    "get_common_error_patterns",
    "troubleshooter_profile"
]
