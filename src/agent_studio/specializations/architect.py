"""Architect Specialization

This module defines a specialization profile for cloud architecture design,
providing expertise in solution architecture, system design, and best practices
across multiple cloud providers.
"""

from typing import Dict, Any, List
from deepagents import SubAgent
from ..base import SpecializationProfile, CloudProvider


ARCHITECT_INSTRUCTIONS = """
You are a Cloud Solutions Architect with deep expertise in designing scalable,
secure, and cost-effective cloud architectures across AWS, GCP, and Azure.

## Core Responsibilities:

### 1. Solution Architecture Design
- Design end-to-end cloud solutions and system architectures
- Create architectural diagrams and documentation
- Define component interactions and data flows
- Establish architectural patterns and standards
- Ensure alignment with business requirements and constraints

### 2. Technology Selection & Integration
- Evaluate and recommend cloud services and technologies
- Design integration patterns and API strategies
- Select appropriate databases, storage, and compute options
- Plan microservices and containerization strategies
- Design event-driven and serverless architectures

### 3. Scalability & Performance Architecture
- Design for horizontal and vertical scaling
- Plan load balancing and traffic distribution
- Architect caching and content delivery strategies
- Design database scaling and partitioning strategies
- Plan capacity and performance optimization

### 4. Security & Compliance Architecture
- Design security-first architectures
- Implement defense-in-depth strategies
- Plan identity and access management architectures
- Design data protection and encryption strategies
- Ensure compliance with regulatory requirements

### 5. Reliability & Disaster Recovery
- Design high-availability and fault-tolerant systems
- Plan disaster recovery and business continuity
- Implement monitoring and observability strategies
- Design backup and restore architectures
- Plan incident response and recovery procedures

### 6. Migration & Modernization
- Design cloud migration strategies and roadmaps
- Plan application modernization approaches
- Design hybrid and multi-cloud architectures
- Plan legacy system integration and retirement
- Design DevOps and CI/CD architectures

## Cloud-Specific Architecture Expertise:

### AWS Architecture:
- Well-Architected Framework pillars
- AWS service selection and integration patterns
- VPC design and network architecture
- IAM and security architecture patterns
- Serverless and container orchestration
- Data lake and analytics architectures
- Multi-region and disaster recovery designs

### GCP Architecture:
- Google Cloud Architecture Framework
- GCP service ecosystem and integration
- VPC and network security design
- Identity and access management patterns
- Cloud-native and Kubernetes architectures
- BigQuery and data analytics designs
- Global load balancing and CDN strategies

### Azure Architecture:
- Azure Well-Architected Framework
- Azure service selection and patterns
- Virtual network and security design
- Azure AD and identity architectures
- Container and microservices patterns
- Data platform and analytics architectures
- Multi-region and availability strategies

## Architecture Design Methodology:

1. **Requirements Analysis**
   - Gather functional and non-functional requirements
   - Understand business constraints and objectives
   - Identify compliance and regulatory requirements
   - Assess current state and technical debt

2. **Architecture Planning**
   - Define architectural principles and patterns
   - Create high-level solution architecture
   - Design detailed component architectures
   - Plan integration and data flow strategies

3. **Technology Selection**
   - Evaluate cloud services and technologies
   - Consider cost, performance, and scalability
   - Assess vendor lock-in and portability
   - Plan technology roadmap and evolution

4. **Design Validation**
   - Review architecture against requirements
   - Validate scalability and performance assumptions
   - Assess security and compliance alignment
   - Conduct architecture reviews and approvals

5. **Implementation Planning**
   - Create implementation roadmap and phases
   - Define deployment and migration strategies
   - Plan testing and validation approaches
   - Establish monitoring and operations procedures

## Architecture Patterns & Best Practices:
- Microservices and service-oriented architectures
- Event-driven and message-based patterns
- CQRS and event sourcing patterns
- API-first and headless architectures
- Infrastructure as Code and GitOps
- Observability and monitoring strategies
- Security by design principles

## Architecture Documentation:
- Solution architecture diagrams
- Component and deployment diagrams
- Data flow and integration diagrams
- Security and network diagrams
- Architecture decision records (ADRs)
- Technical specifications and runbooks

Always provide comprehensive, well-documented architectural solutions with
clear rationale, trade-off analysis, and implementation guidance. Focus on
creating architectures that are scalable, maintainable, and aligned with
business objectives and cloud best practices.
"""


ARCHITECT_SUB_AGENTS = [
    {
        "name": "solution_designer",
        "description": "Designs comprehensive cloud solution architectures",
        "prompt": """
You are a Solution Architecture Designer focused on creating comprehensive cloud solutions.

Focus on:
- End-to-end solution architecture design
- Component selection and integration patterns
- Data flow and system interaction design
- Scalability and performance architecture
- Technology stack recommendations

For each solution design:
- Create detailed architectural diagrams
- Document component responsibilities and interactions
- Provide technology selection rationale
- Include scalability and performance considerations
- Address security and compliance requirements
"""
    },
    {
        "name": "integration_specialist",
        "description": "Designs integration patterns and API strategies",
        "prompt": """
You are an Integration Architecture Specialist focused on system integration and API design.

Focus on:
- API design and integration patterns
- Event-driven architecture design
- Message queue and streaming architectures
- Service mesh and microservices patterns
- Data integration and ETL/ELT strategies

For each integration design:
- Define API contracts and specifications
- Design event flows and message patterns
- Plan data synchronization strategies
- Address integration security and reliability
- Provide implementation and testing guidance
"""
    },
    {
        "name": "infrastructure_planner",
        "description": "Plans cloud infrastructure and deployment architectures",
        "prompt": """
You are an Infrastructure Architecture Planner focused on cloud infrastructure design.

Focus on:
- Cloud infrastructure architecture and sizing
- Network design and security architecture
- Compute, storage, and database planning
- Container orchestration and serverless design
- Infrastructure as Code and automation

For each infrastructure design:
- Size and configure cloud resources
- Design network topology and security
- Plan deployment and scaling strategies
- Address disaster recovery and backup
- Provide cost optimization recommendations
"""
    },
    {
        "name": "migration_strategist",
        "description": "Designs cloud migration and modernization strategies",
        "prompt": """
You are a Cloud Migration Strategist focused on migration and modernization planning.

Focus on:
- Cloud migration strategy and roadmap
- Application modernization approaches
- Legacy system integration and retirement
- Hybrid and multi-cloud architectures
- Risk assessment and mitigation planning

For each migration strategy:
- Assess current state and target architecture
- Design migration phases and dependencies
- Plan modernization and refactoring approaches
- Address data migration and synchronization
- Provide risk mitigation and rollback strategies
"""
    }
]


def create_architect_profile() -> SpecializationProfile:
    """Create an architect specialization profile
    
    Returns:
        SpecializationProfile configured for cloud architecture
    """
    return SpecializationProfile(
        name="architect",
        display_name="Cloud Solutions Architect",
        description="Specializes in designing scalable, secure, and cost-effective cloud architectures",
        version="1.0.0",
        supported_cloud_providers=[
            CloudProvider.AWS,
            CloudProvider.GCP,
            CloudProvider.AZURE
        ],
        instruction_template=ARCHITECT_INSTRUCTIONS,
        sub_agent_configs=ARCHITECT_SUB_AGENTS,
        tool_preferences={
            "architecture_design": ["architecture_center", "solution_templates", "reference_architectures"],
            "cost_estimation": ["pricing_calculator", "cost_estimator", "tco_calculator"],
            "compliance": ["compliance_manager", "security_center", "policy_analyzer"],
            "documentation": ["diagram_tools", "documentation_generator", "adr_templates"]
        },
        required_permissions=[
            "architecture:read",
            "services:list",
            "pricing:read",
            "compliance:read",
            "documentation:write"
        ],
        tags=["architecture", "design", "solution", "planning", "strategy"],
        capabilities=[
            "solution_architecture",
            "technology_selection",
            "integration_design",
            "infrastructure_planning",
            "migration_strategy",
            "architecture_documentation"
        ]
    )


def create_architect_subagents() -> List[SubAgent]:
    """Create sub-agents for architect specialization
    
    Returns:
        List of SubAgent instances for architecture tasks
    """
    return [
        SubAgent(
            name=config["name"],
            description=config["description"],
            prompt=config["prompt"]
        )
        for config in ARCHITECT_SUB_AGENTS
    ]


def get_architecture_frameworks() -> Dict[str, Dict[str, Any]]:
    """Get cloud architecture frameworks and their principles
    
    Returns:
        Dictionary of architecture frameworks with their key principles
    """
    return {
        "aws_well_architected": {
            "name": "AWS Well-Architected Framework",
            "pillars": [
                "Operational Excellence",
                "Security", 
                "Reliability",
                "Performance Efficiency",
                "Cost Optimization",
                "Sustainability"
            ],
            "focus_areas": ["design_principles", "best_practices", "trade_offs", "improvement"]
        },
        "gcp_architecture_framework": {
            "name": "Google Cloud Architecture Framework",
            "pillars": [
                "System Design",
                "Operational Excellence",
                "Security, Privacy, and Compliance",
                "Reliability",
                "Cost Optimization",
                "Performance Optimization"
            ],
            "focus_areas": ["cloud_native", "scalability", "automation", "observability"]
        },
        "azure_well_architected": {
            "name": "Azure Well-Architected Framework",
            "pillars": [
                "Cost Optimization",
                "Operational Excellence",
                "Performance Efficiency",
                "Reliability",
                "Security"
            ],
            "focus_areas": ["design_patterns", "best_practices", "governance", "monitoring"]
        },
        "togaf": {
            "name": "The Open Group Architecture Framework",
            "domains": [
                "Business Architecture",
                "Data Architecture", 
                "Application Architecture",
                "Technology Architecture"
            ],
            "focus_areas": ["enterprise_architecture", "governance", "methodology", "standards"]
        }
    }


def get_architecture_patterns() -> Dict[str, Dict[str, Any]]:
    """Get common cloud architecture patterns
    
    Returns:
        Dictionary of architecture patterns with descriptions and use cases
    """
    return {
        "microservices": {
            "description": "Decompose applications into small, independent services",
            "benefits": ["Scalability", "Technology diversity", "Team autonomy", "Fault isolation"],
            "challenges": ["Complexity", "Network latency", "Data consistency", "Testing"],
            "use_cases": ["Large applications", "Multiple teams", "Diverse technologies", "Independent scaling"]
        },
        "serverless": {
            "description": "Build applications using managed compute services",
            "benefits": ["No server management", "Automatic scaling", "Pay-per-use", "High availability"],
            "challenges": ["Vendor lock-in", "Cold starts", "Limited runtime", "Debugging complexity"],
            "use_cases": ["Event processing", "APIs", "Batch processing", "Real-time data processing"]
        },
        "event_driven": {
            "description": "Architecture based on event production, detection, and consumption",
            "benefits": ["Loose coupling", "Scalability", "Responsiveness", "Flexibility"],
            "challenges": ["Event ordering", "Duplicate handling", "Error handling", "Debugging"],
            "use_cases": ["Real-time processing", "Microservices communication", "IoT", "User activity tracking"]
        },
        "layered": {
            "description": "Organize system into horizontal layers with specific responsibilities",
            "benefits": ["Separation of concerns", "Reusability", "Testability", "Maintainability"],
            "challenges": ["Performance overhead", "Tight coupling", "Complexity", "Data flow"],
            "use_cases": ["Enterprise applications", "Web applications", "Traditional systems", "Monolithic designs"]
        },
        "cqrs": {
            "description": "Separate read and write operations using different models",
            "benefits": ["Performance optimization", "Scalability", "Security", "Flexibility"],
            "challenges": ["Complexity", "Eventual consistency", "Code duplication", "Learning curve"],
            "use_cases": ["High-read applications", "Complex domains", "Event sourcing", "Performance optimization"]
        }
    }


def get_architecture_decision_template() -> Dict[str, str]:
    """Get template for Architecture Decision Records (ADRs)
    
    Returns:
        Dictionary with ADR template structure
    """
    return {
        "title": "ADR-{number}: {short_title}",
        "status": "Proposed | Accepted | Deprecated | Superseded",
        "context": "Describe the architectural decision context and forces at play",
        "decision": "State the architecture decision and rationale",
        "consequences": "Describe the resulting context after applying the decision",
        "alternatives": "List alternative options that were considered",
        "related_decisions": "Reference related ADRs and decisions"
    }


def get_architecture_review_checklist() -> Dict[str, List[str]]:
    """Get architecture review checklist by category
    
    Returns:
        Dictionary of architecture review items organized by category
    """
    return {
        "scalability": [
            "Can the system handle expected load growth?",
            "Are there any single points of failure?",
            "How does the system scale horizontally and vertically?",
            "Are caching strategies appropriate?",
            "Is the database design scalable?"
        ],
        "security": [
            "Are security controls implemented at all layers?",
            "Is data encrypted in transit and at rest?",
            "Are access controls properly implemented?",
            "Is the attack surface minimized?",
            "Are security monitoring and logging adequate?"
        ],
        "reliability": [
            "What is the expected availability and uptime?",
            "How does the system handle failures?",
            "Are backup and recovery procedures defined?",
            "Is monitoring and alerting comprehensive?",
            "Are dependencies and external services managed?"
        ],
        "performance": [
            "Will the system meet performance requirements?",
            "Are there any performance bottlenecks?",
            "Is caching strategy optimal?",
            "Are database queries optimized?",
            "Is network latency minimized?"
        ],
        "cost": [
            "Is the architecture cost-effective?",
            "Are resources right-sized?",
            "Are there opportunities for cost optimization?",
            "Is the pricing model understood?",
            "Are cost monitoring and controls in place?"
        ],
        "maintainability": [
            "Is the architecture well-documented?",
            "Are components loosely coupled?",
            "Is the code and configuration manageable?",
            "Are testing strategies adequate?",
            "Is the deployment process automated?"
        ]
    }


def get_cloud_service_categories() -> Dict[str, Dict[str, List[str]]]:
    """Get cloud service categories by provider
    
    Returns:
        Dictionary of cloud services organized by provider and category
    """
    return {
        "aws": {
            "compute": ["EC2", "Lambda", "ECS", "EKS", "Fargate", "Batch"],
            "storage": ["S3", "EBS", "EFS", "FSx", "Storage Gateway"],
            "database": ["RDS", "DynamoDB", "ElastiCache", "Neptune", "DocumentDB"],
            "networking": ["VPC", "CloudFront", "Route 53", "API Gateway", "Load Balancer"],
            "security": ["IAM", "KMS", "Secrets Manager", "WAF", "Shield"],
            "monitoring": ["CloudWatch", "X-Ray", "Config", "CloudTrail", "Systems Manager"]
        },
        "gcp": {
            "compute": ["Compute Engine", "Cloud Functions", "GKE", "Cloud Run", "App Engine"],
            "storage": ["Cloud Storage", "Persistent Disk", "Filestore", "Cloud SQL"],
            "database": ["Cloud SQL", "Firestore", "Bigtable", "Spanner", "Memorystore"],
            "networking": ["VPC", "Cloud CDN", "Cloud DNS", "API Gateway", "Load Balancing"],
            "security": ["IAM", "KMS", "Secret Manager", "Cloud Armor", "Security Center"],
            "monitoring": ["Cloud Monitoring", "Cloud Logging", "Cloud Trace", "Cloud Profiler"]
        },
        "azure": {
            "compute": ["Virtual Machines", "Functions", "AKS", "Container Instances", "App Service"],
            "storage": ["Blob Storage", "Disk Storage", "Files", "Data Lake Storage"],
            "database": ["SQL Database", "Cosmos DB", "Cache for Redis", "Database for MySQL"],
            "networking": ["Virtual Network", "CDN", "DNS", "API Management", "Load Balancer"],
            "security": ["Active Directory", "Key Vault", "Security Center", "Sentinel"],
            "monitoring": ["Monitor", "Log Analytics", "Application Insights", "Service Health"]
        }
    }


# Export the specialization profile instance
architect_profile = create_architect_profile()

__all__ = [
    "ARCHITECT_INSTRUCTIONS",
    "ARCHITECT_SUB_AGENTS",
    "create_architect_profile",
    "create_architect_subagents",
    "get_architecture_frameworks",
    "get_architecture_patterns",
    "get_architecture_decision_template",
    "get_architecture_review_checklist",
    "get_cloud_service_categories",
    "architect_profile"
]
