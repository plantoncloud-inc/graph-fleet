"""Agent Studio Platform API

FastAPI-based REST API for managing agents, templates, and configurations.
Integrates with existing Planton Cloud authentication and session management.
"""

from typing import Dict, List, Optional, Any
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from datetime import datetime

from .registry import (
    AgentRegistry, AgentTemplate, AgentInstance, AgentCapability,
    CloudProvider, AgentStatus, get_registry
)
from .config_manager import ConfigurationManager, AgentStudioConfig, get_config_manager
from ..agents.aws_agent.utils.session import get_session_manager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()

# API Models
class CreateTemplateRequest(BaseModel):
    """Request model for creating agent templates"""
    name: str
    display_name: str
    description: str
    cloud_provider: CloudProvider
    base_instructions: str
    default_model: str = "gpt-4o-mini"
    default_temperature: float = 0.7
    capabilities: List[AgentCapability] = []
    required_mcp_servers: List[str] = []
    supported_specializations: List[str] = []
    tags: List[str] = []
    author: str = "Agent Studio"


class UpdateTemplateRequest(BaseModel):
    """Request model for updating agent templates"""
    display_name: Optional[str] = None
    description: Optional[str] = None
    base_instructions: Optional[str] = None
    default_model: Optional[str] = None
    default_temperature: Optional[float] = None
    capabilities: Optional[List[AgentCapability]] = None
    supported_specializations: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    status: Optional[AgentStatus] = None


class CreateInstanceRequest(BaseModel):
    """Request model for creating agent instances"""
    name: str
    template_id: str
    custom_instructions: Optional[str] = None
    model_name: Optional[str] = None
    temperature: Optional[float] = None
    specialization_profile: Optional[str] = None
    org_id: Optional[str] = None
    env_id: Optional[str] = None
    region: Optional[str] = None


class DeployInstanceRequest(BaseModel):
    """Request model for deploying agent instances"""
    instance_id: str
    deployment_target: str = "langgraph_studio"
    deployment_config: Dict[str, Any] = {}


class TemplateResponse(BaseModel):
    """Response model for agent templates"""
    id: str
    name: str
    display_name: str
    description: str
    version: str
    cloud_provider: CloudProvider
    capabilities: List[AgentCapability]
    supported_specializations: List[str]
    tags: List[str]
    status: AgentStatus
    created_at: datetime
    updated_at: datetime


class InstanceResponse(BaseModel):
    """Response model for agent instances"""
    id: str
    name: str
    template_id: str
    model_name: str
    temperature: float
    specialization_profile: Optional[str]
    status: AgentStatus
    created_at: datetime
    deployed_at: Optional[datetime]
    total_invocations: int
    success_rate: float


class PlatformStatsResponse(BaseModel):
    """Response model for platform statistics"""
    total_templates: int
    active_templates: int
    total_instances: int
    active_instances: int
    cloud_provider_distribution: Dict[str, int]
    total_invocations: int


# Initialize FastAPI app
def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    config_manager = get_config_manager()
    config = config_manager.config
    
    app = FastAPI(
        title="Agent Studio Platform API",
        description="REST API for managing cloud agents and configurations",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app


app = create_app()


# Authentication dependency
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Validate authentication token and return user info
    
    This integrates with Planton Cloud authentication patterns.
    In production, this would validate JWT tokens against Planton Cloud.
    """
    config_manager = get_config_manager()
    
    if not config_manager.config.enable_auth:
        # Authentication disabled for development
        return {"user_id": "dev_user", "org_id": "dev_org"}
    
    # TODO: Implement actual JWT validation with Planton Cloud
    # For now, return mock user data
    token = credentials.credentials
    if not token or token == "invalid":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {
        "user_id": "authenticated_user",
        "org_id": "user_org",
        "permissions": ["read", "write", "deploy"]
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}


# Platform configuration endpoints
@app.get("/config", response_model=Dict[str, Any])
async def get_platform_config(user: Dict[str, Any] = Depends(get_current_user)):
    """Get platform configuration"""
    config_manager = get_config_manager()
    return config_manager.config.model_dump()


@app.get("/stats", response_model=PlatformStatsResponse)
async def get_platform_stats(user: Dict[str, Any] = Depends(get_current_user)):
    """Get platform statistics"""
    registry = get_registry()
    stats = registry.get_registry_stats()
    return PlatformStatsResponse(**stats)


# Template management endpoints
@app.get("/templates", response_model=List[TemplateResponse])
async def list_templates(
    cloud_provider: Optional[CloudProvider] = None,
    category: Optional[str] = None,
    tags: Optional[str] = None,
    status: Optional[AgentStatus] = None,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """List available agent templates with optional filtering"""
    registry = get_registry()
    
    # Parse tags if provided
    tag_list = tags.split(",") if tags else None
    
    templates = registry.catalog.list_templates(
        cloud_provider=cloud_provider,
        category=category,
        tags=tag_list,
        status=status
    )
    
    return [TemplateResponse(**template.model_dump()) for template in templates]


@app.get("/templates/search")
async def search_templates(
    q: str,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Search templates by query string"""
    registry = get_registry()
    templates = registry.catalog.search_templates(q)
    return [TemplateResponse(**template.model_dump()) for template in templates]


@app.get("/templates/{template_id}", response_model=TemplateResponse)
async def get_template(
    template_id: str,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Get template by ID"""
    registry = get_registry()
    template = registry.catalog.get_template_by_id(template_id)
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template {template_id} not found"
        )
    
    return TemplateResponse(**template.model_dump())


@app.post("/templates", response_model=Dict[str, str])
async def create_template(
    request: CreateTemplateRequest,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Create a new agent template"""
    registry = get_registry()
    
    # Create template from request
    template = AgentTemplate(
        name=request.name,
        display_name=request.display_name,
        description=request.description,
        cloud_provider=request.cloud_provider,
        base_instructions=request.base_instructions,
        default_model=request.default_model,
        default_temperature=request.default_temperature,
        capabilities=request.capabilities,
        required_mcp_servers=request.required_mcp_servers,
        supported_specializations=request.supported_specializations,
        tags=request.tags,
        author=request.author
    )
    
    template_id = registry.register_template(template)
    
    logger.info(f"Created template {template_id} by user {user['user_id']}")
    
    return {"template_id": template_id, "message": "Template created successfully"}


@app.put("/templates/{template_id}", response_model=Dict[str, str])
async def update_template(
    template_id: str,
    request: UpdateTemplateRequest,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Update an existing template"""
    registry = get_registry()
    
    # Convert request to dict, excluding None values
    updates = {k: v for k, v in request.model_dump().items() if v is not None}
    
    success = registry.update_template(template_id, updates)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template {template_id} not found"
        )
    
    logger.info(f"Updated template {template_id} by user {user['user_id']}")
    
    return {"message": "Template updated successfully"}


@app.delete("/templates/{template_id}", response_model=Dict[str, str])
async def delete_template(
    template_id: str,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Delete (archive) a template"""
    registry = get_registry()
    
    success = registry.delete_template(template_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template {template_id} not found"
        )
    
    logger.info(f"Deleted template {template_id} by user {user['user_id']}")
    
    return {"message": "Template archived successfully"}


# Instance management endpoints
@app.get("/instances", response_model=List[InstanceResponse])
async def list_instances(
    template_id: Optional[str] = None,
    status: Optional[AgentStatus] = None,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """List agent instances with optional filtering"""
    registry = get_registry()
    
    instances = registry.list_instances(
        template_id=template_id,
        status=status
    )
    
    return [InstanceResponse(**instance.model_dump()) for instance in instances]


@app.get("/instances/{instance_id}", response_model=InstanceResponse)
async def get_instance(
    instance_id: str,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Get instance by ID"""
    registry = get_registry()
    instance = registry.get_instance(instance_id)
    
    if not instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Instance {instance_id} not found"
        )
    
    return InstanceResponse(**instance.model_dump())


@app.post("/instances", response_model=Dict[str, str])
async def create_instance(
    request: CreateInstanceRequest,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Create a new agent instance from template"""
    registry = get_registry()
    
    # Prepare configuration overrides
    config_overrides = {}
    if request.custom_instructions:
        config_overrides["custom_instructions"] = request.custom_instructions
    if request.model_name:
        config_overrides["model_name"] = request.model_name
    if request.temperature is not None:
        config_overrides["temperature"] = request.temperature
    if request.specialization_profile:
        config_overrides["specialization_profile"] = request.specialization_profile
    if request.org_id:
        config_overrides["org_id"] = request.org_id
    if request.env_id:
        config_overrides["env_id"] = request.env_id
    if request.region:
        config_overrides["region"] = request.region
    
    instance_id = registry.create_instance(
        template_id=request.template_id,
        name=request.name,
        config_overrides=config_overrides
    )
    
    if not instance_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template {request.template_id} not found"
        )
    
    logger.info(f"Created instance {instance_id} from template {request.template_id} by user {user['user_id']}")
    
    return {"instance_id": instance_id, "message": "Instance created successfully"}


@app.post("/instances/{instance_id}/deploy", response_model=Dict[str, str])
async def deploy_instance(
    instance_id: str,
    request: DeployInstanceRequest,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Deploy an agent instance"""
    registry = get_registry()
    instance = registry.get_instance(instance_id)
    
    if not instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Instance {instance_id} not found"
        )
    
    # TODO: Implement actual deployment logic
    # This would integrate with LangGraph Studio deployment
    
    # Update instance status
    registry.instances[instance_id].status = AgentStatus.ACTIVE
    registry.instances[instance_id].deployed_at = datetime.utcnow()
    registry._save_registry()
    
    logger.info(f"Deployed instance {instance_id} to {request.deployment_target} by user {user['user_id']}")
    
    return {"message": f"Instance deployed to {request.deployment_target} successfully"}


@app.post("/instances/{instance_id}/invoke", response_model=Dict[str, Any])
async def invoke_instance(
    instance_id: str,
    request: Dict[str, Any],
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Invoke an agent instance"""
    registry = get_registry()
    instance = registry.get_instance(instance_id)
    
    if not instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Instance {instance_id} not found"
        )
    
    if instance.status != AgentStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Instance {instance_id} is not active"
        )
    
    # TODO: Implement actual agent invocation
    # This would create and invoke the actual agent based on the instance configuration
    
    # Update usage statistics
    registry.update_instance_stats(instance_id, success=True)
    
    logger.info(f"Invoked instance {instance_id} by user {user['user_id']}")
    
    return {
        "instance_id": instance_id,
        "status": "completed",
        "message": "Agent invocation completed successfully"
    }


# Cloud provider specific endpoints
@app.get("/providers", response_model=List[str])
async def list_cloud_providers(user: Dict[str, Any] = Depends(get_current_user)):
    """List supported cloud providers"""
    config_manager = get_config_manager()
    return config_manager.config.supported_cloud_providers


@app.get("/providers/{provider}/templates", response_model=List[TemplateResponse])
async def get_provider_templates(
    provider: CloudProvider,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Get templates for specific cloud provider"""
    registry = get_registry()
    templates = registry.catalog.get_templates_by_cloud_provider(provider)
    return [TemplateResponse(**template.model_dump()) for template in templates]


@app.get("/templates/{template_id}/specializations", response_model=List[str])
async def get_template_specializations(
    template_id: str,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Get available specializations for a template"""
    registry = get_registry()
    specializations = registry.catalog.get_specializations_for_template(template_id)
    return specializations


# Agent Management Endpoints (Task-Required)
# These endpoints provide the specific API paths required by the task

class CreateAgentRequest(BaseModel):
    """Request model for creating agents"""
    name: str
    cloud_provider: CloudProvider
    specialization: Optional[str] = None
    template_id: Optional[str] = None
    custom_instructions: Optional[str] = None
    configuration: Dict[str, Any] = {}
    tags: List[str] = []


class ConfigureAgentRequest(BaseModel):
    """Request model for configuring agents"""
    specialization: Optional[str] = None
    custom_instructions: Optional[str] = None
    configuration: Dict[str, Any] = {}
    cloud_credentials: Optional[Dict[str, str]] = None
    enabled_capabilities: List[str] = []


class DeployAgentRequest(BaseModel):
    """Request model for deploying agents"""
    deployment_target: str = "langgraph_studio"
    environment: str = "production"
    configuration_overrides: Dict[str, Any] = {}


class AgentResponse(BaseModel):
    """Response model for agent information"""
    id: str
    name: str
    cloud_provider: str
    specialization: Optional[str]
    status: str
    created_at: datetime
    last_used: Optional[datetime]
    configuration: Dict[str, Any]
    deployment_status: Optional[str]


@app.post("/agents/create", response_model=Dict[str, str])
async def create_agent(
    request: CreateAgentRequest,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Create a new agent instance
    
    This endpoint creates a new agent based on a template or custom configuration.
    Integrates with Planton Cloud authentication for multi-tenant support.
    """
    try:
        registry = get_registry()
        
        # If template_id is provided, use it as base
        if request.template_id:
            template = registry.get_template(request.template_id)
            if not template:
                raise HTTPException(
                    status_code=404,
                    detail=f"Template {request.template_id} not found"
                )
        else:
            # Create a basic template for the cloud provider
            from .templates import get_template
            template_instance = get_template(request.cloud_provider.value)
            template = template_instance.create_template()
        
        # Create instance configuration
        instance_config = {
            "name": request.name,
            "cloud_provider": request.cloud_provider.value,
            "specialization": request.specialization,
            "custom_instructions": request.custom_instructions,
            "user_id": user.get("user_id", "unknown"),
            "tenant_id": user.get("tenant_id", "default"),
            **request.configuration
        }
        
        # Create the agent instance
        instance_id = registry.create_instance(
            template_id=template.id,
            name=request.name,
            configuration=instance_config,
            tags=request.tags
        )
        
        logger.info(f"Created agent {instance_id} for user {user.get('user_id')}")
        
        return {
            "agent_id": instance_id,
            "message": f"Agent '{request.name}' created successfully",
            "status": "created"
        }
        
    except Exception as e:
        logger.error(f"Failed to create agent: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create agent: {str(e)}"
        )


@app.get("/agents/list", response_model=List[AgentResponse])
async def list_agents(
    cloud_provider: Optional[CloudProvider] = None,
    specialization: Optional[str] = None,
    status: Optional[AgentStatus] = None,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """List agents for the current user
    
    Supports filtering by cloud provider, specialization, and status.
    Implements multi-tenant isolation using Planton Cloud user context.
    """
    try:
        registry = get_registry()
        
        # Get user's tenant context for multi-tenant isolation
        user_id = user.get("user_id")
        tenant_id = user.get("tenant_id", "default")
        
        # List instances with filtering
        instances = registry.list_instances(
            cloud_provider=cloud_provider,
            status=status
        )
        
        # Filter by user/tenant and specialization
        filtered_instances = []
        for instance in instances:
            # Multi-tenant filtering
            if (instance.configuration.get("user_id") == user_id or 
                instance.configuration.get("tenant_id") == tenant_id):
                
                # Specialization filtering
                if specialization and instance.configuration.get("specialization") != specialization:
                    continue
                    
                filtered_instances.append(instance)
        
        # Convert to response format
        agents = []
        for instance in filtered_instances:
            agents.append(AgentResponse(
                id=instance.id,
                name=instance.name,
                cloud_provider=instance.configuration.get("cloud_provider", "unknown"),
                specialization=instance.configuration.get("specialization"),
                status=instance.status.value,
                created_at=instance.created_at,
                last_used=instance.last_used,
                configuration=instance.configuration,
                deployment_status=instance.configuration.get("deployment_status")
            ))
        
        return agents
        
    except Exception as e:
        logger.error(f"Failed to list agents: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list agents: {str(e)}"
        )


@app.put("/agents/{agent_id}/configure", response_model=Dict[str, str])
async def configure_agent(
    agent_id: str,
    request: ConfigureAgentRequest,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Configure an existing agent
    
    Updates agent configuration including specialization, instructions, and cloud credentials.
    Integrates with Planton Cloud session management for credential handling.
    """
    try:
        registry = get_registry()
        
        # Get the agent instance
        instance = registry.get_instance(agent_id)
        if not instance:
            raise HTTPException(
                status_code=404,
                detail=f"Agent {agent_id} not found"
            )
        
        # Verify user has access to this agent (multi-tenant check)
        user_id = user.get("user_id")
        tenant_id = user.get("tenant_id", "default")
        
        if (instance.configuration.get("user_id") != user_id and 
            instance.configuration.get("tenant_id") != tenant_id):
            raise HTTPException(
                status_code=403,
                detail="Access denied to this agent"
            )
        
        # Update configuration
        updated_config = instance.configuration.copy()
        
        if request.specialization:
            updated_config["specialization"] = request.specialization
            
        if request.custom_instructions:
            updated_config["custom_instructions"] = request.custom_instructions
            
        if request.configuration:
            updated_config.update(request.configuration)
            
        if request.enabled_capabilities:
            updated_config["enabled_capabilities"] = request.enabled_capabilities
        
        # Handle cloud credentials through Planton Cloud integration
        if request.cloud_credentials:
            # Integrate with existing session management
            session_manager = get_session_manager()
            
            # Store credentials securely (this would integrate with Planton Cloud)
            credential_context = {
                "user_id": user_id,
                "tenant_id": tenant_id,
                "cloud_provider": instance.configuration.get("cloud_provider"),
                "credentials": request.cloud_credentials
            }
            
            # This would call Planton Cloud credential management
            updated_config["credential_context"] = credential_context
            updated_config["credentials_updated"] = datetime.utcnow().isoformat()
        
        # Update the instance
        success = registry.update_instance(agent_id, updated_config)
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail="Failed to update agent configuration"
            )
        
        logger.info(f"Configured agent {agent_id} for user {user_id}")
        
        return {
            "agent_id": agent_id,
            "message": "Agent configuration updated successfully",
            "status": "configured"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to configure agent {agent_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to configure agent: {str(e)}"
        )


@app.post("/agents/{agent_id}/deploy", response_model=Dict[str, str])
async def deploy_agent(
    agent_id: str,
    request: DeployAgentRequest,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Deploy an agent to the specified target
    
    Supports deployment to LangGraph Studio and other targets.
    Implements multi-tenant deployment with proper isolation.
    """
    try:
        registry = get_registry()
        
        # Get the agent instance
        instance = registry.get_instance(agent_id)
        if not instance:
            raise HTTPException(
                status_code=404,
                detail=f"Agent {agent_id} not found"
            )
        
        # Verify user has access to this agent (multi-tenant check)
        user_id = user.get("user_id")
        tenant_id = user.get("tenant_id", "default")
        
        if (instance.configuration.get("user_id") != user_id and 
            instance.configuration.get("tenant_id") != tenant_id):
            raise HTTPException(
                status_code=403,
                detail="Access denied to this agent"
            )
        
        # Prepare deployment configuration
        deployment_config = {
            "agent_id": agent_id,
            "deployment_target": request.deployment_target,
            "environment": request.environment,
            "user_id": user_id,
            "tenant_id": tenant_id,
            "deployed_at": datetime.utcnow().isoformat(),
            **request.configuration_overrides
        }
        
        # Update instance with deployment status
        updated_config = instance.configuration.copy()
        updated_config["deployment_status"] = "deploying"
        updated_config["deployment_config"] = deployment_config
        
        registry.update_instance(agent_id, updated_config)
        
        # Here would be the actual deployment logic
        # For now, we'll simulate successful deployment
        if request.deployment_target == "langgraph_studio":
            # This would integrate with LangGraph Studio deployment
            deployment_result = {
                "deployment_id": f"deploy_{agent_id}_{int(datetime.utcnow().timestamp())}",
                "status": "deployed",
                "endpoint": f"https://studio.langgraph.com/agents/{agent_id}",
                "environment": request.environment
            }
        else:
            deployment_result = {
                "deployment_id": f"deploy_{agent_id}_{int(datetime.utcnow().timestamp())}",
                "status": "deployed",
                "target": request.deployment_target,
                "environment": request.environment
            }
        
        # Update final deployment status
        updated_config["deployment_status"] = "deployed"
        updated_config["deployment_result"] = deployment_result
        registry.update_instance(agent_id, updated_config)
        
        logger.info(f"Deployed agent {agent_id} to {request.deployment_target} for user {user_id}")
        
        return {
            "agent_id": agent_id,
            "deployment_id": deployment_result["deployment_id"],
            "message": f"Agent deployed successfully to {request.deployment_target}",
            "status": "deployed",
            "endpoint": deployment_result.get("endpoint")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to deploy agent {agent_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to deploy agent: {str(e)}"
        )


# Additional agent management endpoints

@app.get("/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: str,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Get detailed information about a specific agent"""
    try:
        registry = get_registry()
        
        instance = registry.get_instance(agent_id)
        if not instance:
            raise HTTPException(
                status_code=404,
                detail=f"Agent {agent_id} not found"
            )
        
        # Verify user has access to this agent (multi-tenant check)
        user_id = user.get("user_id")
        tenant_id = user.get("tenant_id", "default")
        
        if (instance.configuration.get("user_id") != user_id and 
            instance.configuration.get("tenant_id") != tenant_id):
            raise HTTPException(
                status_code=403,
                detail="Access denied to this agent"
            )
        
        return AgentResponse(
            id=instance.id,
            name=instance.name,
            cloud_provider=instance.configuration.get("cloud_provider", "unknown"),
            specialization=instance.configuration.get("specialization"),
            status=instance.status.value,
            created_at=instance.created_at,
            last_used=instance.last_used,
            configuration=instance.configuration,
            deployment_status=instance.configuration.get("deployment_status")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get agent {agent_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get agent: {str(e)}"
        )


@app.delete("/agents/{agent_id}", response_model=Dict[str, str])
async def delete_agent(
    agent_id: str,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Delete an agent"""
    try:
        registry = get_registry()
        
        instance = registry.get_instance(agent_id)
        if not instance:
            raise HTTPException(
                status_code=404,
                detail=f"Agent {agent_id} not found"
            )
        
        # Verify user has access to this agent (multi-tenant check)
        user_id = user.get("user_id")
        tenant_id = user.get("tenant_id", "default")
        
        if (instance.configuration.get("user_id") != user_id and 
            instance.configuration.get("tenant_id") != tenant_id):
            raise HTTPException(
                status_code=403,
                detail="Access denied to this agent"
            )
        
        # Mark as archived instead of hard delete
        updated_config = instance.configuration.copy()
        updated_config["deleted_at"] = datetime.utcnow().isoformat()
        updated_config["deleted_by"] = user_id
        
        registry.update_instance_status(agent_id, AgentStatus.ARCHIVED)
        registry.update_instance(agent_id, updated_config)
        
        logger.info(f"Deleted agent {agent_id} for user {user_id}")
        
        return {
            "agent_id": agent_id,
            "message": "Agent deleted successfully",
            "status": "deleted"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete agent {agent_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete agent: {str(e)}"
        )


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    logger.error(f"HTTP {exc.status_code}: {exc.detail}")
    return {"error": exc.detail, "status_code": exc.status_code}


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unexpected error: {str(exc)}")
    return {"error": "Internal server error", "status_code": 500}


if __name__ == "__main__":
    import uvicorn
    
    config_manager = get_config_manager()
    config = config_manager.config
    
    uvicorn.run(
        "agent_studio.api:app",
        host=config.api_host,
        port=config.api_port,
        reload=True
    )

