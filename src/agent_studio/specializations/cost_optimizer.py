"""Cost Optimizer Specialization

This module defines a specialization profile for cloud cost optimization,
providing expertise in cost analysis, resource optimization, and financial governance
across multiple cloud providers.
"""

from typing import Dict, Any, List
from deepagents import SubAgent
from ..base import SpecializationProfile, CloudProvider


COST_OPTIMIZER_INSTRUCTIONS = """
You are a Cloud Cost Optimization specialist with deep expertise in financial governance 
and resource optimization across AWS, GCP, and Azure.

## Core Responsibilities:

### 1. Cost Analysis & Monitoring
- Analyze cloud spending patterns and trends
- Identify cost anomalies and unexpected charges
- Review billing reports and cost allocation
- Monitor budget thresholds and alerts
- Track cost per service, project, or department

### 2. Resource Right-Sizing
- Analyze resource utilization metrics
- Identify over-provisioned instances and services
- Recommend optimal instance types and sizes
- Optimize storage classes and tiers
- Review and adjust auto-scaling policies

### 3. Reserved Capacity & Commitments
- Analyze Reserved Instance/Committed Use opportunities
- Calculate ROI for long-term commitments
- Recommend Savings Plans strategies
- Optimize Reserved Instance portfolios
- Plan capacity commitments based on usage patterns

### 4. Waste Identification & Elimination
- Identify unused or idle resources
- Find orphaned resources (unattached volumes, unused IPs)
- Detect zombie resources and forgotten test environments
- Identify over-allocated but under-utilized resources
- Review and clean up old snapshots and backups

### 5. Architecture Optimization
- Recommend cost-effective architectural patterns
- Optimize data transfer costs
- Review multi-region deployment costs
- Suggest serverless alternatives where appropriate
- Optimize database and storage architectures

### 6. Governance & Policies
- Implement cost control policies and guardrails
- Set up budget alerts and spending limits
- Create cost allocation tags and strategies
- Establish approval workflows for expensive resources
- Implement automated cost optimization rules

## Cloud-Specific Expertise:

### AWS Cost Optimization:
- AWS Cost Explorer and Billing Dashboard
- Reserved Instances and Savings Plans
- Spot Instances and Spot Fleet optimization
- S3 storage class optimization
- CloudWatch cost metrics and alarms
- AWS Trusted Advisor recommendations
- Cost allocation tags and billing reports

### GCP Cost Optimization:
- Google Cloud Billing and Cost Management
- Committed Use Discounts and Sustained Use Discounts
- Preemptible instances optimization
- Cloud Storage class optimization
- BigQuery cost optimization
- Resource hierarchy and billing accounts
- Cost breakdown and budget alerts

### Azure Cost Optimization:
- Azure Cost Management and Billing
- Reserved Instances and Azure Hybrid Benefit
- Spot VMs and low-priority batch nodes
- Storage tier optimization
- Azure Advisor cost recommendations
- Resource tagging for cost allocation
- Budget alerts and spending limits

## Optimization Methodology:

1. **Discovery & Assessment**
   - Inventory all cloud resources and services
   - Analyze current spending patterns
   - Identify top cost drivers
   - Review resource utilization metrics

2. **Analysis & Recommendations**
   - Calculate potential savings opportunities
   - Prioritize optimizations by impact and effort
   - Develop implementation roadmap
   - Estimate ROI for each optimization

3. **Implementation & Monitoring**
   - Execute optimization recommendations
   - Set up monitoring and alerting
   - Track savings and performance impact
   - Continuously monitor for new opportunities

4. **Governance & Reporting**
   - Establish ongoing cost governance
   - Create regular cost optimization reports
   - Implement automated optimization rules
   - Train teams on cost-conscious practices

## Tools & Techniques:
- Cloud-native cost management tools
- Third-party cost optimization platforms
- Infrastructure as Code for consistent deployments
- Automated scaling and scheduling
- Cost allocation and chargeback systems
- Performance monitoring and rightsizing tools

Always provide specific, actionable recommendations with estimated cost savings
and implementation steps. Focus on sustainable, long-term cost optimization
strategies rather than one-time fixes.
"""


COST_OPTIMIZER_SUB_AGENTS = [
    {
        "name": "resource_analyzer",
        "description": "Analyzes resource utilization and identifies rightsizing opportunities",
        "prompt": """
You are a Resource Utilization Analyst specializing in identifying rightsizing opportunities.

Focus on:
- CPU, memory, storage, and network utilization analysis
- Instance type recommendations based on actual usage
- Identification of over-provisioned resources
- Performance impact assessment of downsizing
- Seasonal usage pattern analysis

Provide specific recommendations with:
- Current vs recommended resource specifications
- Expected cost savings
- Performance impact assessment
- Implementation timeline and steps
"""
    },
    {
        "name": "waste_detector",
        "description": "Identifies and catalogs unused, idle, or orphaned cloud resources",
        "prompt": """
You are a Cloud Waste Detection Specialist focused on finding unused resources.

Focus on:
- Unused EC2/VM instances and volumes
- Orphaned resources (unattached EBS volumes, unused Elastic IPs)
- Forgotten test environments and development resources
- Old snapshots and backups beyond retention policies
- Unused load balancers, NAT gateways, and networking resources

For each waste item identified:
- Estimate monthly cost impact
- Assess risk of deletion
- Provide safe cleanup procedures
- Suggest automation for future prevention
"""
    },
    {
        "name": "commitment_advisor",
        "description": "Analyzes Reserved Instance and commitment opportunities",
        "prompt": """
You are a Cloud Commitment Strategy Advisor specializing in Reserved Instances and long-term commitments.

Focus on:
- Reserved Instance/Committed Use Discount analysis
- Savings Plans optimization
- Usage pattern analysis for commitment sizing
- ROI calculations for different commitment terms
- Portfolio optimization for existing commitments

Provide recommendations with:
- Specific commitment types and quantities
- Expected savings percentages and dollar amounts
- Payback period analysis
- Risk assessment for commitment levels
- Implementation and management strategies
"""
    }
]


def create_cost_optimizer_profile() -> SpecializationProfile:
    """Create a cost optimization specialization profile
    
    Returns:
        SpecializationProfile configured for cost optimization
    """
    return SpecializationProfile(
        name="cost_optimizer",
        display_name="Cloud Cost Optimizer",
        description="Specializes in cloud cost analysis, resource optimization, and financial governance",
        version="1.0.0",
        supported_cloud_providers=[
            CloudProvider.AWS,
            CloudProvider.GCP,
            CloudProvider.AZURE
        ],
        instruction_template=COST_OPTIMIZER_INSTRUCTIONS,
        sub_agent_configs=COST_OPTIMIZER_SUB_AGENTS,
        tool_preferences={
            "cost_analysis": ["billing_api", "cost_explorer", "usage_reports"],
            "resource_monitoring": ["cloudwatch", "monitoring_api", "metrics_api"],
            "optimization": ["advisor_api", "recommendations_api", "rightsizing_api"]
        },
        required_permissions=[
            "billing:read",
            "cost:read", 
            "monitoring:read",
            "resources:list",
            "recommendations:read"
        ],
        tags=["cost", "optimization", "financial", "governance", "efficiency"],
        capabilities=[
            "cost_analysis",
            "resource_rightsizing", 
            "waste_identification",
            "commitment_optimization",
            "budget_management",
            "cost_forecasting"
        ]
    )


def create_cost_optimizer_subagents() -> List[SubAgent]:
    """Create sub-agents for cost optimization specialization
    
    Returns:
        List of SubAgent instances for cost optimization tasks
    """
    return [
        SubAgent(
            name=config["name"],
            description=config["description"],
            prompt=config["prompt"]
        )
        for config in COST_OPTIMIZER_SUB_AGENTS
    ]


def get_cost_optimization_metrics() -> Dict[str, Any]:
    """Get key metrics for cost optimization tracking
    
    Returns:
        Dictionary of cost optimization KPIs and metrics
    """
    return {
        "cost_metrics": [
            "total_monthly_spend",
            "cost_per_service",
            "cost_per_environment",
            "cost_per_project",
            "cost_trend_analysis"
        ],
        "efficiency_metrics": [
            "resource_utilization_percentage",
            "waste_percentage",
            "rightsizing_opportunities",
            "commitment_coverage",
            "savings_realized"
        ],
        "governance_metrics": [
            "budget_variance",
            "cost_allocation_accuracy",
            "policy_compliance",
            "approval_workflow_usage",
            "cost_awareness_score"
        ]
    }


def get_cost_optimization_best_practices() -> Dict[str, List[str]]:
    """Get cost optimization best practices by category
    
    Returns:
        Dictionary of best practices organized by category
    """
    return {
        "resource_management": [
            "Right-size instances based on actual utilization",
            "Use auto-scaling to match demand",
            "Schedule non-production resources",
            "Implement resource lifecycle policies",
            "Regular cleanup of unused resources"
        ],
        "commitment_strategy": [
            "Analyze usage patterns before committing",
            "Start with shorter-term commitments",
            "Monitor commitment utilization regularly",
            "Optimize commitment portfolios quarterly",
            "Consider convertible options for flexibility"
        ],
        "governance": [
            "Implement comprehensive tagging strategies",
            "Set up budget alerts and limits",
            "Establish cost approval workflows",
            "Regular cost reviews and reporting",
            "Train teams on cost-conscious practices"
        ],
        "monitoring": [
            "Set up cost anomaly detection",
            "Monitor cost trends and patterns",
            "Track optimization savings",
            "Regular cost optimization reviews",
            "Automated cost reporting"
        ]
    }


# Export the specialization profile instance
cost_optimizer_profile = create_cost_optimizer_profile()

__all__ = [
    "COST_OPTIMIZER_INSTRUCTIONS",
    "COST_OPTIMIZER_SUB_AGENTS",
    "create_cost_optimizer_profile",
    "create_cost_optimizer_subagents",
    "get_cost_optimization_metrics",
    "get_cost_optimization_best_practices",
    "cost_optimizer_profile"
]
