"""AWS Error Analysis Tool

This module provides tools for analyzing AWS error messages and providing
troubleshooting guidance based on common error patterns.
"""

from langchain_core.tools import tool


# Common AWS errors and their troubleshooting guidance
COMMON_AWS_ERRORS = {
    "AccessDenied": {
        "guidance": "Check IAM permissions for the service",
        "steps": [
            "Verify the IAM role/user has required permissions",
            "Check if there are any SCPs (Service Control Policies) blocking access",
            "Ensure resource-based policies allow the action",
            "Verify MFA requirements if applicable"
        ]
    },
    "InvalidParameterValue": {
        "guidance": "Verify the parameter values match AWS requirements",
        "steps": [
            "Check parameter format and data types",
            "Verify values are within allowed ranges",
            "Ensure all required parameters are provided",
            "Check for deprecated parameter names"
        ]
    },
    "ResourceNotFound": {
        "guidance": "Ensure the resource exists in the specified region",
        "steps": [
            "Verify the resource ID/ARN is correct",
            "Check if you're in the correct AWS region",
            "Ensure the resource hasn't been deleted",
            "Verify cross-account access if applicable"
        ]
    },
    "ThrottlingException": {
        "guidance": "Request rate exceeded, implement exponential backoff",
        "steps": [
            "Implement retry logic with exponential backoff",
            "Consider request batching where possible",
            "Check service quotas and request increases if needed",
            "Distribute requests across time periods"
        ]
    },
    "ServiceUnavailable": {
        "guidance": "AWS service is temporarily unavailable",
        "steps": [
            "Check AWS Service Health Dashboard",
            "Implement retry logic with backoff",
            "Consider failover to another region if critical",
            "Contact AWS Support if issue persists"
        ]
    }
}


@tool
def analyze_aws_error(error_message: str, service: str) -> str:
    """Analyze AWS error messages and provide troubleshooting guidance
    
    This tool examines AWS error messages to identify common patterns and
    provides specific troubleshooting steps based on the error type and
    the AWS service involved.
    
    Args:
        error_message: The AWS error message to analyze
        service: The AWS service that generated the error (e.g., 'EC2', 'S3', 'ECS')
        
    Returns:
        Detailed analysis with troubleshooting steps
        
    Example:
        >>> analysis = analyze_aws_error(
        ...     "AccessDenied: User is not authorized to perform: s3:GetObject",
        ...     "S3"
        ... )
        >>> print(analysis)
    """
    # Check for known error patterns
    for error_type, info in COMMON_AWS_ERRORS.items():
        if error_type in error_message:
            steps = "\n".join([f"  {i+1}. {step}" for i, step in enumerate(info["steps"])])
            
            return f"""
AWS Error Analysis
==================
Service: {service}
Error Type: {error_type}

Primary Guidance:
{info["guidance"]}

Troubleshooting Steps:
{steps}

Service-Specific Considerations for {service}:
{_get_service_specific_guidance(service, error_type)}

Original Error:
{error_message}
"""
    
    # Generic error analysis
    return f"""
AWS Error Analysis
==================
Service: {service}

This appears to be a service-specific error. General troubleshooting steps:
  1. Check CloudWatch logs for more details
  2. Verify all required parameters and their formats
  3. Review AWS documentation for {service}
  4. Check service quotas and limits
  5. Verify IAM permissions

Original Error:
{error_message}

For detailed analysis, consider checking:
- AWS CloudTrail for API call details
- CloudWatch Logs for application logs
- AWS Support if you have a support plan
"""


def _get_service_specific_guidance(service: str, error_type: str) -> str:
    """Get service-specific guidance for common errors"""
    
    service_guidance = {
        "S3": {
            "AccessDenied": "Check bucket policies, ACLs, and KMS key permissions if encryption is enabled",
            "ResourceNotFound": "Verify bucket name and object key. S3 bucket names are globally unique"
        },
        "EC2": {
            "AccessDenied": "Check VPC permissions, security groups, and instance profile roles",
            "ResourceNotFound": "Ensure instance ID is correct and instance is in the current region"
        },
        "ECS": {
            "AccessDenied": "Verify task execution role and task role permissions",
            "ResourceNotFound": "Check cluster name, service name, and task definition revision"
        },
        "RDS": {
            "AccessDenied": "Check DB subnet group, security groups, and IAM database authentication",
            "ResourceNotFound": "Verify DB instance identifier and ensure it's not in deletion"
        }
    }
    
    if service in service_guidance and error_type in service_guidance[service]:
        return service_guidance[service][error_type]
    
    return f"Review {service}-specific permissions and resource configurations"
