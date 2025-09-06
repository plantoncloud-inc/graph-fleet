# AWS ECS Service Agent

A sophisticated multi-agent system for diagnosing and managing AWS ECS services using natural language interactions and the LangGraph Deep Agents framework.

## Overview

The AWS ECS Service Agent is built on a multi-agent architecture with three specialized components:

- **Contextualizer Agent**: Extracts context from user messages, manages Planton Cloud integration, and handles user interactions
- **Operations Agent**: Executes all AWS ECS-specific operations including triage, planning, remediation, verification, and reporting
- **Supervisor**: Orchestrates the flow between agents and manages the overall conversation state

This system leverages deepagents' built-in capabilities with advanced conversational AI to provide:

- **Conversational Diagnosis**: Accept natural language problem descriptions and collaborate with users to understand ECS issues
- **Context-Aware Operations**: Extract ECS context, user intent, and preferences from conversational interactions
- **Interactive Repair Planning**: Generate minimal, targeted repair plans through collaborative dialogue
- **Automated Diagnosis**: Read-only triage of ECS service issues with user-friendly explanations
- **Safe Execution**: Human-in-the-loop approval for write operations with conversational feedback
- **Comprehensive Reporting**: Markdown reports with audit trails and conversational context
- **MCP Integration**: AWS ECS tools via langchain-mcp-adapters with conversational orchestration
- **Planton Cloud Integration**: Seamless context establishment and credential management through Planton Cloud MCP tools

## Features

### Memory Persistence
- **PostgreSQL Checkpointer**: Persistent conversation memory across sessions
- **Automatic Fallback**: Falls back to in-memory storage if PostgreSQL not configured
- **Thread-level Persistence**: Maintains conversation context and state

### Planton Cloud Integration

The ECS Deep Agent now includes comprehensive Planton Cloud integration for enhanced context establishment and credential management:

#### Context Establishment
- **Automatic Service Discovery**: Leverages Planton Cloud MCP tools to identify ECS services within your organization and environment
- **Credential Management**: Seamlessly retrieves and manages AWS credentials through Planton Cloud
- **Organization Context**: Automatically establishes operational context using organization and environment identifiers
- **Service Identification**: Enhanced service discovery and validation through Planton Cloud service registry

#### New MCP Tools
- **`list_aws_credentials`**: Retrieve available AWS credential summaries from Planton Cloud
- **`get_aws_credential`**: Get complete AWS credential details with proto structure
- **`extract_aws_credentials_for_sdk`**: Extract credentials in flat format for AWS SDK usage
- **`list_aws_ecs_services`**: Identify and enumerate AWS ECS Service cloud resources within specified organization/environment scope
- **`get_aws_ecs_service`**: Get complete AWS ECS Service details with proto structure
- **Enhanced Context Extraction**: Improved natural language processing with Planton Cloud context

#### Configuration
- **`planton_token`**: Authentication token for Planton Cloud API access
- **`org_id`**: Organization identifier for scoped operations
- **`env_name`**: Environment name for targeted service discovery
- **Environment Variable Fallback**: Supports configuration via environment variables for flexible deployment

#### Credential and Service Discovery Workflow
1. **Context Establishment**: Contextualizer calls `list_aws_credentials` and `list_aws_ecs_services` to get summaries
2. **Service Selection**: User or agent selects specific services from the list
3. **Detailed Retrieval**: When operations need full details, call `get_aws_credential` or `get_aws_ecs_service`
4. **SDK Integration**: Use `extract_aws_credentials_for_sdk` to get credentials in flat format for AWS operations

### Agent Architecture

#### Contextualizer Agent
- **Context Extraction**: Parses natural language messages to extract ECS context, problem descriptions, and user intent
- **Planton Cloud Integration**: Automatic service discovery and credential management through Planton Cloud APIs
- **User Interaction Management**: Handles follow-up questions, approvals, and maintains conversation state
- **Flow Orchestration**: Determines when to route conversations to the Operations Agent

#### Operations Agent
The Operations Agent contains specialized sub-agents for comprehensive ECS management:
- **Triage Agent**: Conversation-aware diagnosis and evidence gathering with user-friendly explanations
- **Change Planner**: Creates minimal repair plans incorporating user preferences through interactive dialogue
- **Remediator**: Executes approved changes safely with real-time feedback and user interaction support
- **Verifier**: Post-change verification and health checks with conversational validation
- **Reporter**: Generates comprehensive audit reports with conversational context and collaboration history

#### Supervisor
- **Agent Coordination**: Routes conversations between Contextualizer and Operations agents
- **State Management**: Maintains overall conversation state and context across agent handoffs
- **Safety Orchestration**: Ensures proper approval workflows and safety measures are followed

### Conversational Features

The ECS Deep Agent has been enhanced with advanced conversational capabilities that transform how users interact with ECS troubleshooting:

#### Natural Language Input Processing
- **Problem Description**: Accept plain English descriptions like "My API service is slow and users are complaining"
- **Context Extraction**: Automatically extract ECS identifiers (cluster, service, region) from conversational messages
- **Intent Recognition**: Understand user goals (diagnose, fix, monitor, report) from natural language
- **Symptom Mapping**: Map user-described symptoms to technical ECS issues and diagnostic approaches

#### User Preference Incorporation
- **Risk Tolerance**: Adapt repair approaches based on user's expressed risk comfort level
- **Timing Constraints**: Consider user's maintenance windows and urgency requirements
- **Communication Style**: Adjust technical depth based on user preference (technical, business, mixed)
- **Approval Workflows**: Customize approval processes based on user's operational preferences

#### Real-Time Feedback During Execution
- **Progress Updates**: Provide ongoing status updates during diagnostic and repair phases
- **Action Explanations**: Explain what each subagent is doing and why it matters to the user
- **User Interaction**: Handle questions, concerns, and modification requests during execution
- **Transparent Operations**: Keep users informed of all actions with business-friendly explanations

#### Iterative Conversation Support
- **Multi-Turn Conversations**: Support follow-up questions and iterative problem refinement
- **Context Preservation**: Maintain conversation history and context across multiple interactions
- **Plan Modifications**: Allow users to modify approaches based on changing requirements
- **Session Continuity**: Enable users to return and continue previous troubleshooting sessions

#### Collaborative Troubleshooting
- **Interactive Diagnosis**: Work with users to refine understanding of problems and symptoms
- **Collaborative Planning**: Generate repair plans through dialogue that incorporates user constraints
- **Dynamic Adaptation**: Modify approaches based on user feedback and changing circumstances
- **Knowledge Sharing**: Explain technical findings in user-friendly terms for learning and transparency

### Safety Features
- Write operations disabled by default
- Human approval required for all write operations
- Limited blast radius (only specific ECS operations allowed)
- Comprehensive audit logging

### Supported Operations

**Read Operations** (Always Available):
- `ecs_describe_services`: Get service details and status
- `ecs_describe_tasks`: Get task information and health
- `ecs_list_services`: List services in a cluster
- `ecs_describe_clusters`: Get cluster information
- `logs_get_log_events`: Retrieve CloudWatch logs

**Write Operations** (Requires Approval):
- `ecs_update_service`: Update service desiredCount (±1) or taskDefinition
- `ecs_stop_task`: Stop a single task
- `ecs_run_task`: Run a single task

## Usage

### Via LangGraph Studio

The agent is automatically available in LangGraph Studio as `ecs_deep_agent`.

Configuration options:
- `model_name`: LLM model (default: "claude-3-5-sonnet-20241022")
- `allow_write`: Enable write operations (default: false)
- `allow_sensitive_data`: Handle sensitive data (default: false)
- `aws_region`: AWS region override
- `aws_profile`: AWS profile override

#### Planton Cloud Configuration
- `planton_token`: Authentication token for Planton Cloud API access
- `org_id`: Organization identifier for scoped operations
- `env_name`: Environment name for targeted service discovery

The agent configuration automatically ignores extra fields passed by LangGraph Studio for compatibility.

### Via Programmatic API

```python
from agents.aws_ecs_service import create_ecs_deep_agent, ECSDeepAgentConfig

# Create agent with Planton Cloud integration
config = ECSDeepAgentConfig(
    allow_write=False,  # Safe read-only mode
    planton_token="your-planton-token",
    org_id="your-org-id",
    env_name="your-env-name"
)

agent = await create_ecs_deep_agent(config=config)

# Interact conversationally - agent will automatically establish context
state = {
    "messages": [{"role": "user", "content": "My API service is having issues"}]
}
result = await agent.ainvoke(state)

# The multi-agent system will automatically:
# 1. Contextualizer extracts ECS context and user intent
# 2. Uses Planton Cloud to discover available AWS credentials
# 3. Identifies ECS services in your organization/environment
# 4. Routes to Operations Agent for technical diagnosis and remediation
# 5. Supervisor orchestrates the entire conversation flow
```



## Memory Configuration

### PostgreSQL Checkpointer (Optional)

The ECS Deep Agent supports persistent memory across sessions using PostgreSQL. This allows the agent to maintain conversation context and state between runs.

#### Setup

1. **Install PostgreSQL** (if not already available):
   ```bash
   # Ubuntu/Debian
   sudo apt-get install postgresql postgresql-contrib
   
   # macOS
   brew install postgresql
   
   # Or use a managed service like AWS RDS, Google Cloud SQL, etc.
   ```

2. **Create a database** for the agent:
   ```sql
   CREATE DATABASE ecs_agent_memory;
   CREATE USER ecs_agent WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE ecs_agent_memory TO ecs_agent;
   ```

3. **Set the DATABASE_URL environment variable**:
   ```bash
   export DATABASE_URL="postgresql://ecs_agent:your_password@localhost:5432/ecs_agent_memory"
   ```

#### Connection String Format

The `DATABASE_URL` should follow the PostgreSQL connection string format:
```
postgresql://[user[:password]@][host][:port][/database][?param1=value1&...]
```

Examples:
- Local: `postgresql://user:pass@localhost:5432/dbname`
- AWS RDS: `postgresql://user:pass@mydb.123456789012.us-east-1.rds.amazonaws.com:5432/dbname`
- With SSL: `postgresql://user:pass@host:5432/dbname?sslmode=require`

#### Automatic Fallback

If `DATABASE_URL` is not configured or the PostgreSQL connection fails, the agent automatically falls back to in-memory storage. This ensures the agent continues to work without requiring PostgreSQL setup for basic usage.

## Configuration

### Environment Variables

- `AWS_REGION`: AWS region to use
- `AWS_PROFILE`: AWS profile to use  
- `DATABASE_URL`: PostgreSQL connection string for persistent memory (optional)

#### Planton Cloud Configuration
- `PLANTON_TOKEN`: Authentication token for Planton Cloud API access (optional)
- `PLANTON_ORG_ID`: Organization identifier for scoped operations (optional)
- `PLANTON_ENV_ID`: Environment identifier for targeted service discovery (optional)

### Configuration File

The agent uses `agent.yaml` for configuration:

```yaml
model: "claude-3-5-sonnet-20241022"
allowWrite: false
allowSensitiveData: false
region: ""  # Uses AWS_REGION env var
profile: ""  # Uses AWS_PROFILE env var
```

## Output Files

The agent generates Markdown reports:

- **triage_report.md**: Initial diagnosis with hypotheses and evidence
- **plan_repair_plan.md**: Numbered repair steps with success criteria
- **verify_post_check.md**: Post-change verification results
- **report_summary.md**: Complete timeline and audit trail

## Prerequisites

1. **AWS Credentials**: Configure via AWS CLI or environment variables
2. **AWS API MCP Server**: Automatically installed via `awslabs-aws-api-mcp-server` dependency
3. **PostgreSQL Dependencies**: Automatically installed via `psycopg` and `langgraph-checkpoint-postgres` dependencies (for persistent memory)
4. **Permissions**: ECS read permissions required, write permissions for repairs

## MCP Integration

The ECS Deep Agent uses enhanced MCP integration with both AWS and Planton Cloud:

### AWS API MCP Server
- **AWS API MCP Server**: Uses `awslabs-aws-api-mcp-server` from dependencies
- **ECS-Focused Tools**: Filters AWS API tools to ECS-specific operations  
- **Credential Management**: Supports AWS credentials via environment variables
- **Fallback Support**: Graceful fallback to sub-agents if MCP tools fail

### Planton Cloud MCP Tools
- **Context Establishment**: Automatic service discovery and credential management
- **Organization Scoping**: Operations scoped to specific organization and environment
- **Enhanced Service Discovery**: Improved identification of ECS services and resources
- **Credential Retrieval**: Seamless AWS credential management through Planton Cloud

### Implementation Status
The current implementation includes:
- ✅ Configuration enhancement with Planton Cloud authentication
- ✅ New MCP tool interfaces (`list_aws_credentials`, `get_aws_credential`, `extract_aws_credentials_for_sdk`, `list_aws_ecs_services`, `get_aws_ecs_service`)
- ✅ Enhanced context extractor prompt with Planton Cloud integration
- ✅ Updated state management for context tracking
- 🔄 Placeholder implementations with mock data structures

### Next Steps
- Replace placeholder implementations with actual Planton Cloud RPC calls
- Expand context establishment logic for complex scenarios
- Add comprehensive error handling and user guidance for Planton Cloud integration

### Required AWS Permissions

**Read Operations**:
- `ecs:Describe*`
- `ecs:List*`
- `logs:GetLogEvents`

**Write Operations** (if enabled):
- `ecs:UpdateService`
- `ecs:StopTask`
- `ecs:RunTask`

## Architecture

```
AWS ECS Service Agent (Multi-Agent Architecture)
├── Supervisor (LangGraph)
│   ├── Agent Coordination & Routing
│   ├── State Management
│   └── Safety Orchestration
├── Contextualizer Agent
│   ├── Natural Language Processing
│   ├── Context Extraction (ECS Details, User Intent)
│   ├── Planton Cloud Integration
│   │   ├── Service Discovery
│   │   └── Credential Management
│   └── User Interaction Management
├── Operations Agent
│   ├── Specialized Sub-agents
│   │   ├── Triage Agent (Diagnosis)
│   │   ├── Change Planner (Repair Planning)
│   │   ├── Remediator (Execution)
│   │   ├── Verifier (Validation)
│   │   └── Reporter (Documentation)
│   └── AWS ECS MCP Tools
│       ├── Read Operations (Always Available)
│       └── Write Operations (Gated)
├── Shared Components
│   ├── Conversation State Management
│   ├── Multi-turn History
│   ├── PostgreSQL Persistence (Optional)
│   └── Enhanced Safety Features
└── Integration Points
    ├── LangGraph Studio
    ├── Planton Cloud APIs
    └── AWS ECS APIs
```

### Multi-Agent Flow

```
User Natural Language Input
    ↓
Supervisor (Route to Contextualizer)
    ↓
Contextualizer Agent
├── Parse Intent & Extract ECS Context
├── Planton Cloud Integration (Credentials & Services)
├── User Interaction Management
└── Determine Next Agent (Operations or End)
    ↓
Supervisor (Route to Operations if needed)
    ↓
Operations Agent
┌───────────────────────────────────────────────────────────┐
│                 Operations Sub-agents                     │
│  Triage → Change Planner → Remediator → Verifier → Reporter  │
│  │           │              │           │           │      │
│  └───────────┘──────────────┘───────────┘───────────┘──────┘      │
│     AWS ECS MCP Tools (Read/Write Operations)              │
└───────────────────────────────────────────────────────────┘
    ↓
Supervisor (Coordinate Response & Maintain State)
    ↓
User-friendly Response with Full Context
```

## Examples

### Conversational Usage Patterns

The ECS Deep Agent now supports natural language interactions instead of requiring technical parameters. Here are examples of conversational usage:

#### Initial Problem Report

**User Input:**
```
"My API service in production is responding slowly and users are complaining about timeouts. Can you help me figure out what's wrong?"
```

**Agent Response:**
```
I'll help you diagnose the slow response issues with your API service. Let me extract the context and start investigating.

🔍 Context Extracted:
- Environment: Production
- Service Type: API service
- Symptoms: Slow responses, user timeouts
- Urgency: High (user impact)

🔗 Planton Cloud Context Established:
- Organization: acme-corp
- Environment: production
- Available Services: api-service, worker-service, cache-service
- AWS Credentials: production-account (us-east-1)

I'll now run a comprehensive triage to identify the root cause. This will include:
1. Checking service health and task status for api-service
2. Analyzing resource utilization across production environment
3. Reviewing recent deployment events
4. Examining CloudWatch logs for errors

Starting diagnosis with enhanced context...
```

#### Follow-up Questions and Clarifications

**User Input:**
```
"Actually, the issues started after our deployment yesterday around 3 PM. Could that be related?"
```

**Agent Response:**
```
That's very helpful context! A deployment timing correlation is a strong indicator. Let me focus my analysis on:

🎯 Updated Investigation Plan:
- Comparing pre/post deployment metrics (around 3 PM yesterday)
- Checking if the new task definition has resource constraint issues
- Analyzing deployment events and task replacement patterns
- Looking for configuration changes that might affect performance

This deployment timing makes the investigation much more targeted. Continuing with enhanced focus...
```

#### Interactive Planning and User Preferences

**User Input:**
```
"I found the issue - it's a memory leak in the new code. Can you help me roll back, but I need to be careful because we have a big customer demo at 2 PM today."
```

**Agent Response:**
```
I understand the urgency with your customer demo at 2 PM. Let me create a careful rollback plan that minimizes risk:

📋 Rollback Plan Options:

**Option 1: Conservative Rollback (Recommended)**
- Gradual rollback with 25% traffic shifts
- Monitor between each step
- Total time: ~20 minutes
- Risk: Low, allows quick halt if issues

**Option 2: Quick Rollback**
- Immediate rollback to previous task definition
- Total time: ~5 minutes  
- Risk: Medium, faster but less controlled

Given your demo timing, I recommend Option 1 starting now (11:30 AM) to have everything stable well before 2 PM.

Would you like me to proceed with the conservative approach, or do you prefer the quicker option?
```

#### Real-time Execution Feedback

**User Input:**
```
"Go with the conservative approach, but keep me updated on each step."
```

**Agent Response:**
```
Perfect! Starting conservative rollback with real-time updates:

🔄 **Step 1/4: Preparing Rollback** ✅
- Retrieved previous stable task definition (revision 47)
- Verified task definition is healthy
- Ready to begin traffic shift

🔄 **Step 2/4: First Traffic Shift (25%)** ⏳
- Updating service to 25% new tasks with previous revision
- Current: 75% problematic tasks, 25% stable tasks
- Monitoring response times and error rates...

**Update**: Response times improving! 25% of traffic now on stable revision.
Error rate dropped from 15% to 11%. Continuing to next step...

Would you like me to continue, or do you want to pause and check anything?
```

#### Multi-turn Problem Solving

**User Input:**
```
"Great progress! Continue with the next step, but also can you help me set up monitoring alerts so this doesn't happen again?"
```

**Agent Response:**
```
Absolutely! I'll continue the rollback AND help you set up preventive monitoring.

🔄 **Step 3/4: Second Traffic Shift (50%)** ⏳
- Updating to 50% stable tasks
- Current metrics looking good, proceeding...

📊 **Monitoring Setup Plan** (I'll handle this in parallel):
1. Memory utilization alerts (>80% threshold)
2. Response time degradation alerts (>2x baseline)
3. Error rate spike alerts (>5% increase)
4. Post-deployment health checks automation

The rollback is progressing smoothly. Once complete, I'll implement the monitoring alerts. This way you'll catch similar issues before they impact users.

Current status: 50% traffic now on stable revision, error rate down to 7%!
```

### LangGraph Studio Integration

The AWS ECS Service Agent is designed to work seamlessly with LangGraph Studio for interactive conversational troubleshooting.

**Graph Node Architecture:**
The agent uses properly configured async node functions to avoid coroutine handling issues:
- Contextualizer and Operations nodes are wrapped with proper async handling
- Each node function correctly awaits the underlying agent wrapper functions

```bash
# Start LangGraph Studio
make run  # From the main graph-fleet directory

# Access the agent at http://localhost:8123
# Select 'supervisor' and start conversational interactions
```

## Troubleshooting

### Common Issues

1. **AWS MCP Tools Not Loading**
   ```bash
   # Ensure AWS API MCP server is installed (should be automatic)
   poetry show awslabs-aws-api-mcp-server
   
   # If not installed, reinstall dependencies
   poetry install
   ```

2. **Permission Denied**
   ```bash
   # Check AWS credentials
   aws sts get-caller-identity
   ```

3. **Write Operations Blocked**
   - Configure `allow_write: true` in LangGraph Studio UI
   - Check agent configuration in `agent.yaml`
   - Ensure proper AWS permissions for write operations

4. **PostgreSQL Connection Issues**
   ```bash
   # Check if DATABASE_URL is set correctly
   echo $DATABASE_URL
   
   # Test PostgreSQL connection
   psql $DATABASE_URL -c "SELECT 1;"
   ```
   
   Common solutions:
   - Verify PostgreSQL server is running
   - Check connection string format: `postgresql://user:pass@host:port/dbname`
   - Ensure database and user exist with proper permissions
   - Check firewall/security group settings for remote connections
   - Verify SSL settings if using `sslmode=require`

5. **Memory Persistence Not Working**
   - Agent automatically falls back to in-memory storage if PostgreSQL fails
   - Check logs for "DATABASE_URL not configured" or "Failed to create PostgreSQL checkpointer" messages
   - Ensure `psycopg` and `langgraph-checkpoint-postgres` dependencies are installed:
     ```bash
     poetry show psycopg langgraph-checkpoint-postgres
     ```

### Debug Mode

Enable debug logging for troubleshooting:
```bash
export LOG_LEVEL=DEBUG

# Then start LangGraph Studio to see detailed logs
make run
```

