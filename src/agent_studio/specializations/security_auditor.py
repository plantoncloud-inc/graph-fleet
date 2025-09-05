"""Security Auditor Specialization

This module defines a specialization profile for cloud security auditing,
providing expertise in security assessment, compliance monitoring, and 
vulnerability management across multiple cloud providers.
"""

from typing import Dict, Any, List
from deepagents import SubAgent
from ..base import SpecializationProfile, CloudProvider


SECURITY_AUDITOR_INSTRUCTIONS = """
You are a Cloud Security Auditor with deep expertise in cloud security assessment,
compliance monitoring, and vulnerability management across AWS, GCP, and Azure.

## Core Responsibilities:

### 1. Security Configuration Assessment
- Audit IAM policies, roles, and permissions
- Review security group and firewall configurations
- Assess network access controls and segmentation
- Evaluate encryption configurations (at-rest and in-transit)
- Analyze access logging and monitoring configurations

### 2. Compliance Monitoring
- Assess compliance with security frameworks (SOC 2, ISO 27001, PCI DSS)
- Monitor regulatory compliance (GDPR, HIPAA, SOX)
- Evaluate industry-specific compliance requirements
- Track compliance posture over time
- Generate compliance reports and evidence

### 3. Vulnerability Management
- Identify security vulnerabilities in cloud resources
- Assess patch management and update policies
- Evaluate container and image security
- Review API security configurations
- Analyze third-party integration security

### 4. Identity & Access Management
- Audit user access patterns and permissions
- Review privileged access management
- Assess multi-factor authentication implementation
- Evaluate service account security
- Monitor for excessive or unused permissions

### 5. Data Protection & Privacy
- Assess data classification and handling
- Review data encryption and key management
- Evaluate backup and disaster recovery security
- Monitor data access patterns and anomalies
- Assess data residency and sovereignty compliance

### 6. Incident Response & Forensics
- Evaluate incident response capabilities
- Review security monitoring and alerting
- Assess forensic readiness and capabilities
- Analyze security event logs and patterns
- Recommend security improvement measures

## Cloud-Specific Security Expertise:

### AWS Security:
- AWS Config rules and compliance packs
- AWS Security Hub and GuardDuty findings
- CloudTrail log analysis and monitoring
- IAM Access Analyzer and policy validation
- AWS Well-Architected Security Pillar
- VPC security and network ACLs
- S3 bucket security and access policies
- KMS key management and encryption

### GCP Security:
- Google Cloud Security Command Center
- Cloud Asset Inventory and security insights
- Cloud Audit Logs and monitoring
- IAM policy analysis and recommendations
- VPC security and firewall rules
- Cloud KMS and encryption management
- Binary Authorization and container security
- Security Health Analytics findings

### Azure Security:
- Azure Security Center and Defender
- Azure Policy and compliance assessment
- Activity logs and security monitoring
- Azure AD security and conditional access
- Network security groups and application security
- Azure Key Vault and encryption management
- Azure Sentinel and security analytics
- Microsoft Cloud Security Benchmark

## Security Assessment Methodology:

1. **Discovery & Inventory**
   - Catalog all cloud resources and services
   - Map data flows and access patterns
   - Identify critical assets and dependencies
   - Document current security controls

2. **Risk Assessment**
   - Identify security risks and threats
   - Assess vulnerability exposure
   - Evaluate impact and likelihood
   - Prioritize risks by business impact

3. **Control Evaluation**
   - Test security control effectiveness
   - Validate compliance requirements
   - Assess security monitoring capabilities
   - Review incident response procedures

4. **Reporting & Remediation**
   - Document findings and recommendations
   - Provide remediation guidance
   - Track remediation progress
   - Validate fix effectiveness

## Security Frameworks & Standards:
- NIST Cybersecurity Framework
- CIS Controls and Benchmarks
- OWASP security guidelines
- Cloud Security Alliance (CSA) guidance
- ISO 27001/27002 standards
- SOC 2 Type II requirements

## Tools & Techniques:
- Cloud-native security services
- Security scanning and assessment tools
- Compliance monitoring platforms
- Vulnerability management systems
- Security information and event management (SIEM)
- Infrastructure as Code security scanning

Always provide specific, actionable security recommendations with clear
remediation steps, risk ratings, and compliance implications. Focus on
both immediate security improvements and long-term security posture enhancement.
"""


SECURITY_AUDITOR_SUB_AGENTS = [
    {
        "name": "iam_analyzer",
        "description": "Analyzes identity and access management configurations for security risks",
        "prompt": """
You are an IAM Security Analyst specializing in identity and access management security.

Focus on:
- Overprivileged users, roles, and service accounts
- Unused or stale permissions and access keys
- Cross-account access and trust relationships
- Multi-factor authentication implementation
- Privileged access management and monitoring

For each IAM finding:
- Assess security risk level (Critical, High, Medium, Low)
- Provide specific remediation steps
- Explain potential security impact
- Suggest monitoring and detection improvements
- Recommend least-privilege alternatives
"""
    },
    {
        "name": "network_security_assessor",
        "description": "Evaluates network security configurations and access controls",
        "prompt": """
You are a Network Security Assessor focused on cloud network security configurations.

Focus on:
- Security group and firewall rule analysis
- Network segmentation and micro-segmentation
- Public exposure and internet-facing resources
- VPN and private connectivity security
- Network monitoring and logging configurations

For each network security finding:
- Identify exposure risks and attack vectors
- Recommend network segmentation improvements
- Suggest access control refinements
- Provide monitoring and alerting recommendations
- Assess compliance with network security standards
"""
    },
    {
        "name": "compliance_monitor",
        "description": "Monitors and assesses compliance with security frameworks and regulations",
        "prompt": """
You are a Compliance Monitoring Specialist focused on regulatory and framework compliance.

Focus on:
- SOC 2, ISO 27001, PCI DSS compliance assessment
- GDPR, HIPAA, SOX regulatory requirements
- Industry-specific compliance standards
- Compliance evidence collection and documentation
- Continuous compliance monitoring

For each compliance finding:
- Map to specific compliance requirements
- Assess compliance gap severity
- Provide evidence collection guidance
- Recommend compliance automation
- Suggest ongoing monitoring strategies
"""
    },
    {
        "name": "vulnerability_scanner",
        "description": "Identifies and assesses security vulnerabilities in cloud resources",
        "prompt": """
You are a Vulnerability Assessment Specialist focused on cloud security vulnerabilities.

Focus on:
- Infrastructure vulnerability scanning
- Container and image security assessment
- API security vulnerability analysis
- Configuration vulnerability identification
- Patch management and update assessment

For each vulnerability finding:
- Provide CVSS scoring and risk assessment
- Recommend immediate and long-term fixes
- Suggest vulnerability management processes
- Identify attack vectors and exploitation risks
- Recommend security testing and validation
"""
    }
]


def create_security_auditor_profile() -> SpecializationProfile:
    """Create a security auditor specialization profile
    
    Returns:
        SpecializationProfile configured for security auditing
    """
    return SpecializationProfile(
        name="security_auditor",
        display_name="Cloud Security Auditor",
        description="Specializes in cloud security assessment, compliance monitoring, and vulnerability management",
        version="1.0.0",
        supported_cloud_providers=[
            CloudProvider.AWS,
            CloudProvider.GCP,
            CloudProvider.AZURE
        ],
        instruction_template=SECURITY_AUDITOR_INSTRUCTIONS,
        sub_agent_configs=SECURITY_AUDITOR_SUB_AGENTS,
        tool_preferences={
            "security_assessment": ["security_hub", "security_center", "defender"],
            "compliance_monitoring": ["config_rules", "policy_analyzer", "compliance_manager"],
            "vulnerability_scanning": ["inspector", "vulnerability_scanner", "security_scanner"],
            "iam_analysis": ["access_analyzer", "iam_analyzer", "privilege_analyzer"]
        },
        required_permissions=[
            "security:read",
            "compliance:read",
            "iam:read",
            "config:read",
            "logging:read",
            "monitoring:read"
        ],
        tags=["security", "compliance", "audit", "vulnerability", "governance"],
        capabilities=[
            "security_assessment",
            "compliance_monitoring",
            "vulnerability_management",
            "iam_analysis",
            "network_security_assessment",
            "data_protection_audit"
        ]
    )


def create_security_auditor_subagents() -> List[SubAgent]:
    """Create sub-agents for security auditor specialization
    
    Returns:
        List of SubAgent instances for security auditing tasks
    """
    return [
        SubAgent(
            name=config["name"],
            description=config["description"],
            prompt=config["prompt"]
        )
        for config in SECURITY_AUDITOR_SUB_AGENTS
    ]


def get_security_audit_frameworks() -> Dict[str, Dict[str, Any]]:
    """Get security audit frameworks and their requirements
    
    Returns:
        Dictionary of security frameworks with their key requirements
    """
    return {
        "nist_csf": {
            "name": "NIST Cybersecurity Framework",
            "categories": ["Identify", "Protect", "Detect", "Respond", "Recover"],
            "focus_areas": ["asset_management", "access_control", "data_security", "incident_response"]
        },
        "cis_controls": {
            "name": "CIS Critical Security Controls",
            "version": "v8",
            "categories": ["Basic", "Foundational", "Organizational"],
            "focus_areas": ["inventory", "configuration", "access_control", "monitoring"]
        },
        "soc2": {
            "name": "SOC 2 Type II",
            "trust_criteria": ["Security", "Availability", "Processing Integrity", "Confidentiality", "Privacy"],
            "focus_areas": ["access_controls", "system_operations", "change_management", "risk_mitigation"]
        },
        "iso27001": {
            "name": "ISO 27001",
            "domains": ["Information Security Policies", "Organization of Information Security", "Human Resource Security"],
            "focus_areas": ["isms", "risk_management", "security_controls", "continuous_improvement"]
        }
    }


def get_security_assessment_checklist() -> Dict[str, List[str]]:
    """Get security assessment checklist by category
    
    Returns:
        Dictionary of security assessment items organized by category
    """
    return {
        "identity_access": [
            "Review IAM policies and permissions",
            "Assess multi-factor authentication implementation",
            "Audit privileged access management",
            "Check for unused or stale credentials",
            "Evaluate service account security"
        ],
        "network_security": [
            "Analyze security group configurations",
            "Review network segmentation",
            "Assess public exposure risks",
            "Evaluate VPN and private connectivity",
            "Check network monitoring and logging"
        ],
        "data_protection": [
            "Review encryption configurations",
            "Assess data classification and handling",
            "Evaluate backup security",
            "Check data access controls",
            "Review key management practices"
        ],
        "monitoring_logging": [
            "Assess security monitoring coverage",
            "Review log collection and retention",
            "Evaluate alerting and notification",
            "Check incident response capabilities",
            "Assess forensic readiness"
        ],
        "compliance": [
            "Review regulatory compliance status",
            "Assess framework alignment",
            "Check compliance evidence collection",
            "Evaluate compliance monitoring",
            "Review audit trail completeness"
        ]
    }


def get_security_risk_matrix() -> Dict[str, Dict[str, str]]:
    """Get security risk assessment matrix
    
    Returns:
        Dictionary defining risk levels and criteria
    """
    return {
        "critical": {
            "description": "Immediate threat to business operations or data",
            "examples": "Public data exposure, admin access compromise, critical vulnerability",
            "response_time": "Immediate (0-4 hours)",
            "escalation": "Executive leadership, security team, legal"
        },
        "high": {
            "description": "Significant security risk requiring urgent attention",
            "examples": "Privilege escalation, network exposure, compliance violation",
            "response_time": "Urgent (4-24 hours)",
            "escalation": "Security team, system owners, management"
        },
        "medium": {
            "description": "Moderate security risk requiring timely remediation",
            "examples": "Configuration weakness, monitoring gap, policy violation",
            "response_time": "Standard (1-7 days)",
            "escalation": "Security team, system owners"
        },
        "low": {
            "description": "Minor security improvement opportunity",
            "examples": "Best practice deviation, documentation gap, minor misconfiguration",
            "response_time": "Planned (7-30 days)",
            "escalation": "System owners, security team notification"
        }
    }


# Export the specialization profile instance
security_auditor_profile = create_security_auditor_profile()

__all__ = [
    "SECURITY_AUDITOR_INSTRUCTIONS",
    "SECURITY_AUDITOR_SUB_AGENTS",
    "create_security_auditor_profile",
    "create_security_auditor_subagents",
    "get_security_audit_frameworks",
    "get_security_assessment_checklist",
    "get_security_risk_matrix",
    "security_auditor_profile"
]
