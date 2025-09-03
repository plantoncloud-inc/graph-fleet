"""AWS Architecture Generation Tool

This module provides tools for generating AWS architecture recommendations
based on system requirements and best practices.
"""

from langchain_core.tools import tool


@tool
def generate_aws_architecture(requirements: str) -> str:
    """Generate AWS architecture recommendations based on requirements
    
    This tool analyzes system requirements and provides AWS architecture
    recommendations following the Well-Architected Framework principles.
    
    Args:
        requirements: Description of the system requirements, including:
            - Expected traffic/load
            - Data storage needs
            - Security requirements
            - Budget constraints
            - Compliance needs
        
    Returns:
        Comprehensive architecture recommendations with AWS services
        
    Example:
        >>> arch = generate_aws_architecture(
        ...     "E-commerce platform, 100k daily users, PCI compliance needed"
        ... )
    """
    # Parse requirements to identify key patterns
    req_lower = requirements.lower()
    
    # Determine workload characteristics
    is_web_app = any(term in req_lower for term in ["web", "api", "rest", "http", "portal"])
    is_high_traffic = any(term in req_lower for term in ["high traffic", "100k", "million", "scale"])
    needs_compliance = any(term in req_lower for term in ["pci", "hipaa", "sox", "compliance", "regulated"])
    is_realtime = any(term in req_lower for term in ["realtime", "real-time", "streaming", "websocket"])
    needs_ml = any(term in req_lower for term in ["ml", "machine learning", "ai", "prediction"])
    
    # Build architecture recommendations
    arch_components = []
    
    # Compute layer
    if is_web_app and is_high_traffic:
        arch_components.append("""
**Compute Layer:**
- ECS Fargate or EKS for containerized microservices
- Application Load Balancer (ALB) for HTTP/HTTPS traffic
- Auto Scaling based on CPU/memory metrics
- Consider Lambda for event-driven components""")
    elif is_web_app:
        arch_components.append("""
**Compute Layer:**
- EC2 with Auto Scaling Groups
- Elastic Load Balancer (ALB for HTTP, NLB for TCP)
- Consider Elastic Beanstalk for simple deployments""")
    else:
        arch_components.append("""
**Compute Layer:**
- Lambda for serverless processing
- Step Functions for workflow orchestration
- Batch for large-scale batch processing""")
    
    # Storage layer
    arch_components.append("""
**Storage Layer:**
- S3 for object storage (static assets, backups, data lake)
- EBS for EC2 block storage (use gp3 for cost optimization)
- EFS for shared file storage across instances
- CloudFront CDN for global content delivery""")
    
    # Database layer
    if needs_compliance:
        arch_components.append("""
**Database Layer:**
- RDS with Multi-AZ for relational data (PostgreSQL/MySQL)
- Enable encryption at rest and in transit
- Automated backups with point-in-time recovery
- DynamoDB for session storage and real-time data""")
    else:
        arch_components.append("""
**Database Layer:**
- Aurora Serverless v2 for variable workloads
- DynamoDB for NoSQL requirements
- ElastiCache (Redis) for caching and sessions
- Consider RDS Proxy for connection pooling""")
    
    # Networking
    arch_components.append("""
**Networking & Security:**
- VPC with public/private subnets across multiple AZs
- NAT Gateway for outbound internet access from private subnets
- Security Groups as virtual firewalls (least privilege)
- Network ACLs for subnet-level security
- AWS WAF for web application protection""")
    
    # Security and compliance
    if needs_compliance:
        arch_components.append("""
**Security & Compliance:**
- AWS Config for compliance monitoring
- CloudTrail for audit logging (to S3 with lifecycle policies)
- Systems Manager for patch management
- Secrets Manager for credentials and API keys
- KMS for encryption key management
- Shield Standard (DDoS protection)""")
    
    # Monitoring
    arch_components.append("""
**Monitoring & Operations:**
- CloudWatch for metrics, logs, and alarms
- X-Ray for distributed tracing
- CloudWatch Synthetics for endpoint monitoring
- AWS Cost Explorer for cost optimization
- Systems Manager for operational tasks""")
    
    # Special considerations
    special_considerations = []
    
    if is_realtime:
        special_considerations.append("""
**Real-time Components:**
- WebSocket API via API Gateway
- AppSync for GraphQL subscriptions
- Kinesis for data streaming
- IoT Core for device connectivity""")
    
    if needs_ml:
        special_considerations.append("""
**Machine Learning Components:**
- SageMaker for model training and deployment
- Rekognition/Textract for vision/document AI
- Comprehend for NLP tasks
- S3 + Glue for data preparation""")
    
    # Cost optimization tips
    cost_tips = """
**Cost Optimization Tips:**
1. Use Savings Plans or Reserved Instances for predictable workloads
2. Implement lifecycle policies for S3 storage classes
3. Use Spot Instances for fault-tolerant workloads
4. Enable Cost Allocation Tags for detailed tracking
5. Set up budget alerts in AWS Budgets"""
    
    # Combine all components
    architecture = f"""
# AWS Architecture Recommendations

**Requirements Analysis:**
{requirements}

## Recommended Architecture Components:

{"".join(arch_components)}

{"".join(special_considerations)}

{cost_tips}

## Architecture Patterns:
- **High Availability**: Multi-AZ deployment with auto-failover
- **Scalability**: Horizontal scaling with load balancing
- **Security**: Defense in depth with multiple security layers
- **Cost Efficiency**: Right-sizing and automated resource management

## Next Steps:
1. Create detailed architecture diagram
2. Define specific resource configurations
3. Estimate costs using AWS Pricing Calculator
4. Plan phased implementation approach
5. Set up proof of concept for validation

**Note**: For detailed design, consider using sub-agents specialized in specific AWS services.
"""
    
    return architecture
