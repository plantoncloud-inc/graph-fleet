# Session Subject Generator Agent

## Overview

The Session Subject Generator is a lightweight LangGraph agent that generates meaningful, concise session subjects (titles) based on the user's first message and agent metadata. It's designed to replace auto-generated timestamp subjects with contextual, human-readable titles.

## Purpose

When users start a new session with an agent, the session is initially created with a timestamp-based subject like "Session 2025-10-31_14-30-45". This agent generates more meaningful subjects like "PostgreSQL Database Setup" or "RDS Multi-AZ Configuration" based on the actual conversation content.

## Usage

This is an **internal-only agent** used by the Planton Cloud agent fleet system. It is not exposed to end users directly. The agent is invoked asynchronously by the `agent-fleet-worker` service during the first execution of a session.

### Integration Flow

1. User starts a new session with an agent
2. Agent-fleet-worker detects this is the first execution
3. Worker invokes session subject generator asynchronously (non-blocking)
4. Generated subject updates the session via gRPC
5. User sees meaningful subject in UI instead of timestamp

## Input Format

The agent expects a JSON input with three fields:

```json
{
  "user_message": "I need to set up a PostgreSQL database with Multi-AZ for production",
  "agent_name": "RDS Manifest Generator",
  "agent_description": "Helps users create AWS RDS Instance manifests through conversational interface"
}
```

### Input Fields

- **user_message** (string, required): The user's first message in the session
- **agent_name** (string, required): Name of the agent being used
- **agent_description** (string, required): Description of what the agent does

## Output Format

The agent returns a JSON object with the generated subject:

```json
{
  "subject": "PostgreSQL Multi-AZ Production Setup"
}
```

### Output Field

- **subject** (string): Generated session subject following these rules:
  - 3-7 words maximum
  - 50 characters maximum
  - No pronouns (your, this, that, their)
  - No "Session" prefix
  - Descriptive of task/intent
  - Professional but friendly tone
  - Title case

## Subject Generation Guidelines

### Good Subjects

✅ **"PostgreSQL Database Setup"**
- Concise, descriptive, clear intent

✅ **"RDS Multi-AZ Configuration"**
- Includes key technical details

✅ **"Deploy Kubernetes Cluster"**
- Action-oriented, specific

✅ **"Configure AWS Networking"**
- Clear scope and platform

✅ **"Debug Production API Error"**
- Indicates urgency and context

✅ **"Optimize React Performance"**
- Specific technology and goal

### Bad Subjects

❌ **"Your PostgreSQL Setup"**
- Contains pronoun "your"

❌ **"This is a session about configuring RDS"**
- Too wordy, contains pronouns

❌ **"Session: Deploy Cluster"**
- Contains "Session" prefix (redundant in UI)

❌ **"Help me with something"**
- Too vague, not descriptive

❌ **"I need to configure my database instance for production use"**
- Too long (exceeds 50 chars)

## Example Scenarios

### Scenario 1: RDS Database Setup

**Input:**
```json
{
  "user_message": "I want to create a production PostgreSQL database with encryption and Multi-AZ",
  "agent_name": "RDS Manifest Generator",
  "agent_description": "Creates AWS RDS Instance manifests"
}
```

**Output:**
```json
{
  "subject": "PostgreSQL Multi-AZ Encrypted Database"
}
```

### Scenario 2: Kubernetes Deployment

**Input:**
```json
{
  "user_message": "Help me deploy a Node.js application to Kubernetes with autoscaling",
  "agent_name": "Kubernetes Deployment Agent",
  "agent_description": "Assists with Kubernetes deployments"
}
```

**Output:**
```json
{
  "subject": "Node.js Kubernetes Autoscaling Deploy"
}
```

### Scenario 3: Troubleshooting

**Input:**
```json
{
  "user_message": "My API is returning 500 errors in production and I need to debug it",
  "agent_name": "Debug Assistant",
  "agent_description": "Helps diagnose and fix production issues"
}
```

**Output:**
```json
{
  "subject": "Debug Production API 500 Errors"
}
```

### Scenario 4: Configuration

**Input:**
```json
{
  "user_message": "I need to set up VPC networking with subnets and security groups",
  "agent_name": "AWS Network Configurator",
  "agent_description": "Configures AWS networking resources"
}
```

**Output:**
```json
{
  "subject": "AWS VPC Network Configuration"
}
```

## Technical Details

### Architecture

- **Type**: Simple React agent (LangGraph + LangChain)
- **Model**: Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`)
- **Max Tokens**: 1000 (short output)
- **Tools**: None (pure LLM generation)
- **Middleware**: None (no external dependencies)

### Graph Structure

Simple linear flow:
```
START → generate_subject → END
```

No conditional edges or complex routing needed.

### State Schema

```python
class SessionSubjectState(TypedDict):
    # Input fields
    user_message: str
    agent_name: str
    agent_description: str
    
    # Output field
    subject: str
```

### Performance

- **Generation Time**: ~2-5 seconds
- **Execution**: Asynchronous (non-blocking)
- **Retry Policy**: 2 attempts max
- **Timeout**: 30 seconds

## Deployment

The agent is deployed to LangGraph Cloud as part of the graph-fleet service. It's registered in `langgraph.json`:

```json
{
  "graphs": {
    "session_subject_generator": "src.agents.session_subject_generator.graph:graph"
  }
}
```

### Invocation

The agent is invoked via HTTP POST to the LangGraph Cloud endpoint:

```
POST https://langgraph-cloud.planton.cloud/session_subject_generator/invoke
```

## Error Handling

Subject generation failures:
- Log error with context
- Do not fail main execution
- Leave timestamp subject as fallback
- Retry once (max 2 attempts)

## Limitations

- Only processes the first message (subsequent messages don't update subject)
- Subject length capped at 50 characters
- No support for custom subject templates
- English language only

## Future Enhancements

Potential improvements:
- Multi-language support
- Custom subject templates per agent
- Subject regeneration on user request
- Learning from user edits to subjects
- A/B testing different subject styles

## Related Documentation

- Master Plan: `.cursor/plans/session-subject-generator-12eb6f51.plan.md`
- Phase 1 Plan: `.cursor/plans/phase-1-session-subject-generator-aa0b9ca4.plan.md`
- Agent Fleet Architecture: See planton-cloud backend services

## Support

For issues or questions about this agent:
- Check LangGraph Cloud logs: `_cursor/langgraph-cloud-server-logs`
- Review Temporal workflow logs in agent-fleet-worker
- Contact: engineering@planton.cloud

