# AWS ECS Troubleshooting Agent

## Project Overview
**Start Date**: September 22, 2025  
**Target Completion**: September 29, 2025 (1 week)  
**Project Type**: Feature Development - New Agent Capability

## Description
Build an autonomous MCP-based agent for AWS ECS Service troubleshooting that integrates with Planton Cloud to establish context, retrieve AWS credentials, and diagnose/fix ECS service issues using the Langgraph framework.

## Primary Goal
Create a production-ready autonomous agent that can troubleshoot and fix AWS ECS Service issues by leveraging Planton Cloud context and AWS MCP tools, minimizing user interaction and maximizing self-healing capabilities.

## Key Features
- **Autonomous Operation**: Minimal user interaction, automatic context gathering
- **Self-Healing**: Attempts to fix issues automatically (with user approval)
- **Context-Aware**: Leverages Planton Cloud for service metadata and credentials
- **Comprehensive Diagnostics**: Analyzes logs, metrics, task definitions, and configurations

## Technology Stack
- **Language**: Python with async/await patterns
- **Framework**: Langgraph for agent orchestration
- **MCP Tools**: 
  - AWS MCP tools (existing)
  - Planton Cloud MCP tools (existing)
  - Additional tools as needed
- **Integration**: Graph Fleet framework

## Success Criteria
1. ✅ Agent successfully diagnoses common ECS service issues autonomously
2. ✅ Proper context setup from Planton Cloud without user intervention
3. ✅ Secure credential handling and AWS connection establishment
4. ✅ Clear error messages and troubleshooting recommendations
5. ✅ **Autonomous remediation**: Attempts to fix issues with user approval

## Architecture Flow

### 1. User Input Phase
- User: "I have an issue with AWS ECS Service X"
- Agent acknowledges and begins autonomous investigation

### 2. Context Setup Phase (Autonomous)
- Query Planton Cloud for service metadata
- Retrieve appropriate AWS credentials
- Establish AWS connection with proper region/account
- Gather all relevant context without asking user

### 3. Troubleshooting Phase (Autonomous)
- Use AWS MCP tools to inspect ECS service
- Analyze:
  - Task definitions and configurations
  - Service logs and events
  - Container health and resource utilization
  - Network configurations
  - IAM permissions
  - Load balancer health (if applicable)
- Identify root causes

### 4. Remediation Phase (With Approval)
- Generate fix proposals for identified issues
- Present clear remediation plan to user
- Upon approval, execute fixes
- Verify resolution
- Fallback to recommendations if auto-fix not possible

## Project Components
- `/src/agents/aws_ecs_troubleshooter/` - Main agent implementation
- `/src/planton_cloud_mcp/connect/` - Context setup utilities
- `/src/workflows/ecs_diagnostics/` - Langgraph workflow definitions
- `/tests/` - Unit and integration tests

## Dependencies
- AWS MCP tools (available)
- Planton Cloud MCP tools (available)
- Langgraph framework (in use)
- Additional MCP tools can be added as needed

## Risks & Mitigation
1. **Credential Management Security**
   - Mitigation: Use secure credential retrieval from Planton Cloud
   - Never log or expose credentials

2. **Context Setup Complexity**
   - Mitigation: Build robust fallback mechanisms
   - Clear error messages when context cannot be established

3. **Error Handling for AWS/ECS Failures**
   - Mitigation: Comprehensive error catching
   - Graceful degradation when auto-fix not possible

4. **Integration Testing**
   - Mitigation: Create mock environments
   - Test with various failure scenarios

## Timeline
- **Week 1 (Sep 22-29)**: MVP with core troubleshooting capabilities
  - Days 1-2: Architecture design and context setup
  - Days 3-4: Core diagnostic implementation
  - Days 5-6: Auto-remediation features
  - Day 7: Testing and refinement
- **Post-MVP**: Incremental feature additions based on user feedback

## Special Requirements
- Must use Langgraph framework
- Must not reinvent existing MCP tools
- Follow planning → review → implementation process
- Prioritize autonomous operation
- Minimize user interactions

## Notes
- Remove all existing code in `/src/agents/aws_ecs_service/` before implementation
- Focus on autonomous operation - only ask for clarification when absolutely necessary
- Auto-fix capability is preferred but can fallback to recommendations in v1

## Quick Links
- [Next Task](./next-task.md)
- [Task Planning](./tasks/)
- [Design Decisions](./design-decisions/)
- [Checkpoints](./checkpoints/)
