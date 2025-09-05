"""Base Agent State System

This module provides cloud-agnostic base classes for agent state that extend
the existing AWSAgentState patterns to support multiple cloud providers and
specialized agent variants while maintaining compatibility with DeepAgents.
"""

from typing import Optional, Dict, Any, List
from pydantic import Field
from datetime import datetime

# Import DeepAgentState and existing AWS patterns
from deepagents import DeepAgentState
from ...agents.aws_agent.state import AWSAgentState
from .base_agent_config import CloudProvider, SpecializationProfile


class BaseAgentState(DeepAgentState):
    """Base state for cloud agents extending DeepAgentState patterns
    
    This state includes all DeepAgent fields plus cloud-agnostic extensions:
    - Multi-cloud credential management
    - Specialization tracking
    - Session context management
    - Cross-cloud compatibility
    """
    
    # Cloud provider and specialization
    cloud_provider: Optional[CloudProvider] = Field(
        default=None,
        description="Current cloud provider for this agent session"
    )
    
    specialization_profile: Optional[SpecializationProfile] = Field(
        default=None,
        description="Active specialization profile"
    )
    
    # Multi-cloud credential management
    selected_credential_id: Optional[str] = Field(
        default=None,
        description="Currently selected cloud credential ID"
    )
    
    selected_credential_summary: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Summary of selected credential (id, name, account/project, region)"
    )
    
    credential_expires_at: Optional[int] = Field(
        default=None,
        description="Unix timestamp when credentials expire (for temporary credentials)"
    )
    
    selection_version: int = Field(
        default=0,
        description="Monotonic counter for credential selection changes"
    )
    
    # Session context (Planton Cloud integration)
    org_id: Optional[str] = Field(
        default=None,
        description="Planton Cloud organization ID"
    )
    
    env_id: Optional[str] = Field(
        default=None,
        description="Planton Cloud environment ID (optional)"
    )
    
    actor_token: Optional[str] = Field(
        default=None,
        description="Actor token for Planton Cloud API calls"
    )
    
    # Cloud-specific context
    current_region: Optional[str] = Field(
        default=None,
        description="Current region for cloud operations"
    )
    
    available_regions: List[str] = Field(
        default=[],
        description="List of available regions for current cloud provider"
    )
    
    # Sub-agent tracking
    active_sub_agents: List[str] = Field(
        default=[],
        description="List of currently active sub-agent names"
    )
    
    sub_agent_results: Dict[str, Any] = Field(
        default={},
        description="Results from completed sub-agent operations"
    )
    
    # Specialization context
    specialization_context: Dict[str, Any] = Field(
        default={},
        description="Context specific to the current specialization"
    )
    
    # Multi-cloud operation tracking
    cross_cloud_operations: List[Dict[str, Any]] = Field(
        default=[],
        description="Track operations that span multiple cloud providers"
    )
    
    # Session metadata
    session_start_time: Optional[datetime] = Field(
        default=None,
        description="When the current session started"
    )
    
    last_activity_time: Optional[datetime] = Field(
        default=None,
        description="Last activity timestamp"
    )
    
    operation_count: int = Field(
        default=0,
        description="Number of operations performed in this session"
    )
    
    # Error tracking and recovery
    last_error: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Information about the last error encountered"
    )
    
    retry_count: int = Field(
        default=0,
        description="Number of retries for current operation"
    )
    
    # Tool and MCP context
    available_mcp_tools: List[str] = Field(
        default=[],
        description="List of currently available MCP tools"
    )
    
    mcp_server_status: Dict[str, str] = Field(
        default={},
        description="Status of MCP servers (server_name -> status)"
    )
    
    def to_aws_state(self) -> AWSAgentState:
        """Convert to AWSAgentState for backward compatibility
        
        Returns:
            AWSAgentState instance with compatible fields
            
        Raises:
            ValueError: If current cloud provider is not AWS
        """
        if self.cloud_provider and self.cloud_provider != CloudProvider.AWS:
            raise ValueError("Cannot convert non-AWS state to AWSAgentState")
        
        # Create AWS-specific state with mapped fields
        aws_state = AWSAgentState(
            # Copy DeepAgent fields
            messages=self.messages,
            # Map credential fields
            selectedCredentialId=self.selected_credential_id,
            selectedCredentialSummary=self.selected_credential_summary,
            stsExpiresAt=self.credential_expires_at,
            selectionVersion=self.selection_version,
            # Map session fields
            orgId=self.org_id,
            envId=self.env_id,
            actorToken=self.actor_token,
            awsRegion=self.current_region or "us-east-1"
        )
        
        # Copy any additional DeepAgent fields that might exist
        for field_name, field_value in self.model_dump().items():
            if hasattr(aws_state, field_name) and field_name not in [
                'messages', 'selectedCredentialId', 'selectedCredentialSummary',
                'stsExpiresAt', 'selectionVersion', 'orgId', 'envId', 
                'actorToken', 'awsRegion'
            ]:
                setattr(aws_state, field_name, field_value)
        
        return aws_state
    
    @classmethod
    def from_aws_state(cls, aws_state: AWSAgentState) -> 'BaseAgentState':
        """Create BaseAgentState from AWSAgentState
        
        Args:
            aws_state: AWSAgentState instance to convert
            
        Returns:
            BaseAgentState instance with mapped fields
        """
        # Extract AWS-specific fields and map to base fields
        base_state = cls(
            # Copy DeepAgent fields
            messages=aws_state.messages,
            # Map credential fields
            cloud_provider=CloudProvider.AWS,
            selected_credential_id=aws_state.selectedCredentialId,
            selected_credential_summary=aws_state.selectedCredentialSummary,
            credential_expires_at=aws_state.stsExpiresAt,
            selection_version=aws_state.selectionVersion,
            # Map session fields
            org_id=aws_state.orgId,
            env_id=aws_state.envId,
            actor_token=aws_state.actorToken,
            current_region=aws_state.awsRegion
        )
        
        # Copy any additional DeepAgent fields
        for field_name, field_value in aws_state.model_dump().items():
            if hasattr(base_state, field_name) and field_name not in [
                'messages', 'selectedCredentialId', 'selectedCredentialSummary',
                'stsExpiresAt', 'selectionVersion', 'orgId', 'envId', 
                'actorToken', 'awsRegion'
            ]:
                setattr(base_state, field_name, field_value)
        
        return base_state
    
    def update_credential_selection(
        self, 
        credential_id: str, 
        credential_summary: Dict[str, Any],
        expires_at: Optional[int] = None
    ) -> None:
        """Update credential selection information
        
        Args:
            credential_id: New credential ID
            credential_summary: Summary information about the credential
            expires_at: Optional expiration timestamp for temporary credentials
        """
        self.selected_credential_id = credential_id
        self.selected_credential_summary = credential_summary
        self.credential_expires_at = expires_at
        self.selection_version += 1
        self.last_activity_time = datetime.utcnow()
        
        # Update region if provided in summary
        if credential_summary and 'defaultRegion' in credential_summary:
            self.current_region = credential_summary['defaultRegion']
    
    def clear_credential_selection(self) -> None:
        """Clear current credential selection"""
        self.selected_credential_id = None
        self.selected_credential_summary = None
        self.credential_expires_at = None
        self.selection_version += 1
        self.last_activity_time = datetime.utcnow()
    
    def is_credential_expired(self) -> bool:
        """Check if current credentials are expired
        
        Returns:
            True if credentials are expired or will expire soon
        """
        if not self.credential_expires_at:
            return False
        
        # Consider credentials expired if they expire within 5 minutes
        current_time = datetime.utcnow().timestamp()
        return current_time >= (self.credential_expires_at - 300)
    
    def add_sub_agent(self, sub_agent_name: str) -> None:
        """Add an active sub-agent
        
        Args:
            sub_agent_name: Name of the sub-agent to add
        """
        if sub_agent_name not in self.active_sub_agents:
            self.active_sub_agents.append(sub_agent_name)
            self.last_activity_time = datetime.utcnow()
    
    def remove_sub_agent(self, sub_agent_name: str, result: Optional[Any] = None) -> None:
        """Remove an active sub-agent and optionally store its result
        
        Args:
            sub_agent_name: Name of the sub-agent to remove
            result: Optional result from the sub-agent operation
        """
        if sub_agent_name in self.active_sub_agents:
            self.active_sub_agents.remove(sub_agent_name)
            
            if result is not None:
                self.sub_agent_results[sub_agent_name] = result
            
            self.last_activity_time = datetime.utcnow()
    
    def update_specialization_context(self, key: str, value: Any) -> None:
        """Update specialization-specific context
        
        Args:
            key: Context key
            value: Context value
        """
        self.specialization_context[key] = value
        self.last_activity_time = datetime.utcnow()
    
    def get_specialization_context(self, key: str, default: Any = None) -> Any:
        """Get specialization-specific context value
        
        Args:
            key: Context key
            default: Default value if key not found
            
        Returns:
            Context value or default
        """
        return self.specialization_context.get(key, default)
    
    def record_operation(self) -> None:
        """Record that an operation was performed"""
        self.operation_count += 1
        self.last_activity_time = datetime.utcnow()
        self.retry_count = 0  # Reset retry count on successful operation
    
    def record_error(self, error_type: str, error_message: str, error_details: Optional[Dict[str, Any]] = None) -> None:
        """Record an error that occurred
        
        Args:
            error_type: Type of error
            error_message: Error message
            error_details: Optional additional error details
        """
        self.last_error = {
            "type": error_type,
            "message": error_message,
            "details": error_details or {},
            "timestamp": datetime.utcnow().isoformat(),
            "operation_count": self.operation_count
        }
        self.retry_count += 1
        self.last_activity_time = datetime.utcnow()
    
    def clear_error(self) -> None:
        """Clear the last error"""
        self.last_error = None
        self.retry_count = 0
    
    def update_mcp_tools(self, tools: List[str]) -> None:
        """Update the list of available MCP tools
        
        Args:
            tools: List of available tool names
        """
        self.available_mcp_tools = tools
        self.last_activity_time = datetime.utcnow()
    
    def update_mcp_server_status(self, server_name: str, status: str) -> None:
        """Update MCP server status
        
        Args:
            server_name: Name of the MCP server
            status: Status of the server (e.g., 'connected', 'disconnected', 'error')
        """
        self.mcp_server_status[server_name] = status
        self.last_activity_time = datetime.utcnow()
    
    def add_cross_cloud_operation(self, operation: Dict[str, Any]) -> None:
        """Add a cross-cloud operation record
        
        Args:
            operation: Operation details including source/target clouds, operation type, etc.
        """
        operation_record = {
            **operation,
            "timestamp": datetime.utcnow().isoformat(),
            "session_operation_count": self.operation_count
        }
        self.cross_cloud_operations.append(operation_record)
        self.last_activity_time = datetime.utcnow()
    
    def get_session_duration(self) -> Optional[float]:
        """Get session duration in seconds
        
        Returns:
            Session duration in seconds, or None if session start time not set
        """
        if not self.session_start_time:
            return None
        
        current_time = self.last_activity_time or datetime.utcnow()
        return (current_time - self.session_start_time).total_seconds()
    
    def initialize_session(self) -> None:
        """Initialize a new session"""
        self.session_start_time = datetime.utcnow()
        self.last_activity_time = datetime.utcnow()
        self.operation_count = 0
        self.retry_count = 0
        self.last_error = None
        self.active_sub_agents = []
        self.sub_agent_results = {}
        self.cross_cloud_operations = []
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get a summary of the current session
        
        Returns:
            Dictionary with session statistics and information
        """
        return {
            "cloud_provider": self.cloud_provider.value if self.cloud_provider else None,
            "specialization_profile": self.specialization_profile.value if self.specialization_profile else None,
            "session_duration": self.get_session_duration(),
            "operation_count": self.operation_count,
            "active_sub_agents": len(self.active_sub_agents),
            "completed_sub_agents": len(self.sub_agent_results),
            "cross_cloud_operations": len(self.cross_cloud_operations),
            "has_credentials": self.selected_credential_id is not None,
            "credentials_expired": self.is_credential_expired(),
            "last_error": self.last_error is not None,
            "available_tools": len(self.available_mcp_tools),
            "mcp_servers": len(self.mcp_server_status)
        }


class CloudAgentState(BaseAgentState):
    """Specialized state for cloud-specific agents
    
    This extends BaseAgentState with additional cloud-specific functionality
    while maintaining compatibility with existing patterns.
    """
    
    # Cloud-specific resource tracking
    managed_resources: Dict[str, List[str]] = Field(
        default={},
        description="Resources managed by this agent (resource_type -> [resource_ids])"
    )
    
    resource_operations: List[Dict[str, Any]] = Field(
        default=[],
        description="History of resource operations performed"
    )
    
    # Cost and billing context
    cost_context: Dict[str, Any] = Field(
        default={},
        description="Cost-related context and tracking information"
    )
    
    # Security and compliance context
    security_context: Dict[str, Any] = Field(
        default={},
        description="Security and compliance related context"
    )
    
    # Performance and monitoring context
    performance_context: Dict[str, Any] = Field(
        default={},
        description="Performance monitoring and optimization context"
    )
    
    def add_managed_resource(self, resource_type: str, resource_id: str) -> None:
        """Add a managed resource
        
        Args:
            resource_type: Type of resource (e.g., 'ec2_instance', 'gcs_bucket')
            resource_id: Unique identifier for the resource
        """
        if resource_type not in self.managed_resources:
            self.managed_resources[resource_type] = []
        
        if resource_id not in self.managed_resources[resource_type]:
            self.managed_resources[resource_type].append(resource_id)
            self.last_activity_time = datetime.utcnow()
    
    def remove_managed_resource(self, resource_type: str, resource_id: str) -> bool:
        """Remove a managed resource
        
        Args:
            resource_type: Type of resource
            resource_id: Resource identifier to remove
            
        Returns:
            True if resource was removed, False if not found
        """
        if resource_type in self.managed_resources:
            if resource_id in self.managed_resources[resource_type]:
                self.managed_resources[resource_type].remove(resource_id)
                self.last_activity_time = datetime.utcnow()
                return True
        return False
    
    def record_resource_operation(
        self, 
        operation_type: str, 
        resource_type: str, 
        resource_id: str,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """Record a resource operation
        
        Args:
            operation_type: Type of operation (create, update, delete, etc.)
            resource_type: Type of resource
            resource_id: Resource identifier
            details: Optional operation details
        """
        operation = {
            "operation_type": operation_type,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "details": details or {},
            "timestamp": datetime.utcnow().isoformat(),
            "session_operation_count": self.operation_count
        }
        
        self.resource_operations.append(operation)
        self.record_operation()
    
    def get_resources_by_type(self, resource_type: str) -> List[str]:
        """Get managed resources of a specific type
        
        Args:
            resource_type: Type of resource to retrieve
            
        Returns:
            List of resource IDs of the specified type
        """
        return self.managed_resources.get(resource_type, [])
    
    def get_all_managed_resources(self) -> Dict[str, List[str]]:
        """Get all managed resources
        
        Returns:
            Dictionary mapping resource types to lists of resource IDs
        """
        return self.managed_resources.copy()
    
    def update_cost_context(self, key: str, value: Any) -> None:
        """Update cost-related context
        
        Args:
            key: Context key
            value: Context value
        """
        self.cost_context[key] = value
        self.last_activity_time = datetime.utcnow()
    
    def update_security_context(self, key: str, value: Any) -> None:
        """Update security-related context
        
        Args:
            key: Context key
            value: Context value
        """
        self.security_context[key] = value
        self.last_activity_time = datetime.utcnow()
    
    def update_performance_context(self, key: str, value: Any) -> None:
        """Update performance-related context
        
        Args:
            key: Context key
            value: Context value
        """
        self.performance_context[key] = value
        self.last_activity_time = datetime.utcnow()
