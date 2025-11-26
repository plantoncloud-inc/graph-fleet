# Testing Guide: AWS RDS Instance Creator

This document provides comprehensive testing scenarios for the AWS RDS Instance Creator agent.

## Prerequisites

Before testing, ensure:

1. **Environment Setup**:
   ```bash
   # Create .env file with your API key
   PLANTON_API_KEY=your_api_key_here
   PLANTON_CLOUD_ENVIRONMENT=live
   ```

2. **Network Connectivity**:
   - Ensure you have internet access
   - Verify https://mcp.planton.ai/ is reachable

3. **Dependencies Installed**:
   ```bash
   make deps
   ```

## Starting the Agent

```bash
cd /Users/suresh/scm/github.com/plantoncloud-inc/graph-fleet
make run
# Open http://localhost:8123
# Select 'aws_rds_instance_creator' from dropdown
```

## Test Scenarios

### Scenario 1: Complete Initial Request

**Purpose**: Test the agent's ability to extract all requirements from a comprehensive initial message.

**Input**:
```
Create a production PostgreSQL 15.5 RDS instance with:
- Instance class: db.m5.large
- Storage: 200GB
- Multi-AZ enabled
- Username: prodadmin
- Organization: my-company
- Environment: production
- Name: prod-postgres-main
```

**Expected Behavior**:
1. Agent calls `get_cloud_resource_schema` to understand schema
2. Extracts all fields from message
3. May ask for password or offer to auto-generate
4. Summarizes configuration
5. Asks for confirmation
6. Calls `create_cloud_resource`
7. Reports success with resource ID

**Success Criteria**:
- [ ] All fields extracted correctly
- [ ] Minimal follow-up questions needed
- [ ] Resource created successfully
- [ ] Resource ID returned

### Scenario 2: Incomplete Initial Request

**Purpose**: Test conversational flow when requirements are missing.

**Input**:
```
I need a MySQL database for development
```

**Expected Behavior**:
1. Recognizes engine=mysql, use case=development
2. Asks for missing fields conversationally:
   - Instance class (suggests db.t3.small for dev)
   - MySQL version (suggests 8.0)
   - Storage size
   - Organization and environment
3. Collects responses naturally
4. Summarizes and confirms
5. Creates the instance

**Success Criteria**:
- [ ] Natural conversation flow
- [ ] Helpful suggestions provided
- [ ] All required fields collected
- [ ] Resource created successfully

### Scenario 3: Validation Error Handling

**Purpose**: Test error handling when invalid values are provided.

**Input**:
```
Create PostgreSQL RDS with:
- Instance class: t3.large (missing 'db.' prefix)
- Storage: -10 (invalid negative value)
- Engine version: 99.9 (non-existent version)
```

**Expected Behavior**:
1. Agent attempts to create with provided values
2. Receives validation error from server
3. Explains error conversationally:
   - "Instance class needs to start with 'db.' - did you mean db.t3.large?"
   - "Storage must be greater than 0. How much would you like?"
   - "Engine version 99.9 doesn't exist. Would you like 15.5 (latest stable)?"
4. Collects corrections
5. Retries successfully

**Success Criteria**:
- [ ] Errors caught and explained clearly
- [ ] Helpful corrections suggested
- [ ] Successful retry after fixes
- [ ] User not frustrated by errors

### Scenario 4: Different Database Engines

**Purpose**: Test support for all RDS engine types.

**Test Cases**:

**A. PostgreSQL**:
```
Create PostgreSQL 15.5 database with db.t3.small, 20GB storage
```

**B. MySQL**:
```
Create MySQL 8.0 database with db.t3.medium, 50GB storage
```

**C. MariaDB**:
```
Create MariaDB 10.6 database with db.t3.micro, 20GB storage
```

**Expected**: All engine types supported, appropriate version suggestions.

**Success Criteria**:
- [ ] PostgreSQL creation works
- [ ] MySQL creation works  
- [ ] MariaDB creation works
- [ ] Correct engine-specific defaults suggested

### Scenario 5: Environment and Organization Selection

**Purpose**: Test organization and environment handling.

**Input**:
```
Create a PostgreSQL database. I'm not sure which environment to use.
```

**Expected Behavior**:
1. Agent asks for organization
2. Offers to list available environments: "I can show you the available environments in your organization"
3. Calls `list_environments_for_org` if user agrees
4. Displays environments
5. User selects one
6. Proceeds with creation

**Success Criteria**:
- [ ] Environment listing offered
- [ ] MCP tool called correctly
- [ ] Environments displayed clearly
- [ ] User can select from list

### Scenario 6: Resource Name Handling

**Purpose**: Test custom vs auto-generated names.

**Test A - Custom Name**:
```
Create PostgreSQL RDS named 'analytics-db'
```
**Expected**: Uses 'analytics-db' as resource name

**Test B - Auto-Generated**:
```
Create PostgreSQL RDS (no name specified)
```
**Expected**: Generates name like 'postgres-production-a4f2c1'

**Success Criteria**:
- [ ] Custom names respected
- [ ] Auto-generated names follow pattern
- [ ] Names are valid (lowercase, hyphens)

### Scenario 7: Password Handling

**Purpose**: Test password auto-generation vs user-provided.

**Test A - Auto-Generate**:
```
Create PostgreSQL RDS, auto-generate the password
```
**Expected**: Password not requested, auto-generated by Planton Cloud

**Test B - User-Provided**:
```
Create PostgreSQL RDS with username 'admin' and password 'SecurePass123!'
```
**Expected**: Uses provided credentials

**Success Criteria**:
- [ ] Auto-generation works
- [ ] User-provided passwords accepted
- [ ] Security best practices explained

### Scenario 8: Multi-AZ Configuration

**Purpose**: Test high availability option handling.

**Input**:
```
Create production PostgreSQL RDS with high availability
```

**Expected Behavior**:
1. Recognizes "high availability" means multi-AZ
2. Explains cost implications
3. Confirms user wants multi-AZ despite higher cost
4. Creates with multiAz: true

**Success Criteria**:
- [ ] Multi-AZ understood from various phrasings
- [ ] Cost tradeoff explained
- [ ] Confirmation obtained
- [ ] Correct configuration applied

## Negative Test Cases

### Test 1: Missing API Key

**Setup**: Remove `PLANTON_API_KEY` from environment

**Expected**: 
- Clear error message during agent initialization
- Helpful instructions to set API key

### Test 2: Invalid Organization

**Input**: Use non-existent organization name

**Expected**:
- Error from MCP server
- Agent explains organization doesn't exist or user lacks access
- Suggests verifying organization name

### Test 3: MCP Server Not Available

**Setup**: Block network access or use invalid API endpoint

**Expected**:
- Agent fails to initialize
- Clear error about connection failure
- Instructions to verify connectivity

## Performance Testing

### Response Time

**Test**: Measure time from user message to agent response

**Targets**:
- Initial schema fetch: < 2 seconds
- Follow-up questions: < 1 second
- Resource creation: < 5 seconds (excluding AWS provisioning time)

### Conversation Efficiency

**Metric**: Number of back-and-forth exchanges needed

**Targets**:
- Complete initial request: 2-3 exchanges (summary → confirmation → success)
- Incomplete request: 4-6 exchanges (questions → answers → summary → confirmation → success)

## Success Criteria Summary

For the agent to be considered production-ready:

- [ ] All 8 positive scenarios pass
- [ ] All 3 negative test cases handled gracefully  
- [ ] Response times meet targets
- [ ] Conversation feels natural and helpful
- [ ] Error messages are clear and actionable
- [ ] No linting or type errors
- [ ] Documentation is complete and accurate

## Manual Testing Checklist

When testing manually:

1. **Start Fresh**:
   - [ ] Clean terminal
   - [ ] Fresh LangGraph Studio session
   - [ ] Verify internet connectivity to mcp.planton.ai

2. **For Each Scenario**:
   - [ ] Copy input exactly
   - [ ] Observe agent behavior
   - [ ] Note any unexpected responses
   - [ ] Verify resource created (if applicable)
   - [ ] Check Planton Cloud console for resource

3. **Document Issues**:
   - Screenshot unexpected behavior
   - Copy full conversation logs
   - Note environment details

## Automated Testing (Future)

Potential areas for automation:

1. **Unit Tests**: Test MCP tool loading logic
2. **Integration Tests**: Mock MCP server responses
3. **E2E Tests**: Use LangGraph test framework
4. **Regression Tests**: Ensure fixes don't break existing scenarios

## Known Limitations

Current known limitations to test around:

1. **AWS Provisioning Time**: Actual RDS creation takes 10-15 minutes (not agent's fault)
2. **MCP Server Dependency**: Agent can't function without MCP server
3. **API Rate Limits**: Too many rapid creations may hit limits
4. **Schema Changes**: Agent relies on current RDS schema structure

## Troubleshooting During Testing

### Agent doesn't appear in dropdown
- Check `langgraph.json` has correct entry
- Run `make build` to check for errors
- Restart LangGraph Studio

### MCP tools not loading
- Verify internet connectivity to https://mcp.planton.ai/
- Check API key in `.env`
- Look for errors in terminal output
- Test API key works: try accessing Planton Cloud console

### Validation errors
- Check field name casing (camelCase)
- Verify required fields present
- Review schema with `get_cloud_resource_schema`

### Resource not appearing in console
- Wait 30-60 seconds for propagation
- Verify correct organization and environment
- Check user has permission to view resources

---

**Testing Status**: ⚠️ Manual testing required

**Next Steps**:
1. Complete manual testing of all scenarios
2. Document any issues found
3. Fix bugs and retest
4. Mark as production-ready when all criteria met

