# Phase 4: Authentication Documentation Updates

**Date**: November 27, 2025

## Summary

Completed comprehensive documentation updates for Phase 4 of the Dynamic Per-User MCP Authentication project, transforming all graph-fleet documentation to reflect the new per-user authentication model. Created two major new developer resources (Developer Guide and Authentication Architecture docs) totaling 1,700+ lines, updated existing documentation across 3 files, and eliminated all references to required static API keys in production documentation. This work ensures developers can successfully build custom agents with proper authentication patterns and understand the complete security architecture.

## Problem Statement

Phase 4 documentation was the final piece of the authentication implementation (following Phases 0-3 which implemented the actual token flow). The existing documentation was outdated and misleading:

### Pain Points

- **Outdated Prerequisites**: Documentation still required `PLANTON_API_KEY` for all scenarios, implying it was needed in production
- **No Developer Guidance**: No comprehensive guide for developers building custom agents with the new authentication pattern
- **Missing Architecture Documentation**: The token flow and security model were not documented, making it hard to understand or troubleshoot
- **Confusing Local vs Production**: Documentation didn't distinguish between production (automatic auth) and local development (optional test token)
- **No Security Context**: Developers didn't understand why per-user authentication mattered or how to implement it correctly
- **Agent-Specific Docs Out of Date**: AWS RDS Instance Creator README still described static API key authentication
- **No Copy-Paste Examples**: Developers had to reverse-engineer the authentication pattern from existing code

## Solution

Created and updated comprehensive documentation that clearly separates production (automatic authentication) from local development (optional test credentials), provides complete implementation guidance for custom agent developers, and explains the security architecture in detail.

### Documentation Strategy

**Two-Track Approach**:
1. **User-Facing Documentation**: Updated READMEs to emphasize that authentication is automatic in production
2. **Developer-Facing Documentation**: Created detailed guides for building custom agents with proper authentication

**Key Principles**:
- Production-first: Emphasize that authentication "just works" when deployed
- Local development as optional: Test credentials only needed for LangGraph Studio testing
- Security-aware: Explain why per-user auth matters and how to implement it correctly
- Copy-paste friendly: Provide working code examples developers can use directly

## Implementation Details

### 1. Main Graph-Fleet README Updates

**File**: `graph-fleet/README.md`

**Changes**:

- **New Authentication Section** (35 lines): Added comprehensive section explaining production vs. local development authentication
  - Production: Automatic, no configuration needed
  - Local: Optional `PLANTON_API_KEY` for testing
  - Security model benefits clearly listed

- **Updated MCP Integration Section**: Transformed from generic description to specific explanation of per-user authentication pattern
  - Before: Generic "creates credentials"
  - After: Specific "dynamic Authorization headers with user JWT"

- **Enhanced "Adding a New Agent"**: Added requirement to follow per-user authentication pattern with link to Developer Guide
  - Added step about MCP tool authentication requirements
  - Added link to comprehensive Developer Guide
  - Emphasized testing in staging for multi-user scenarios

**Code Example from README**:
```markdown
### Production (Planton Cloud)

When deployed on Planton Cloud, authentication is **fully automatic**:

- User JWT tokens are automatically extracted from incoming requests
- Tokens propagate through the execution stack to MCP tools
- Each MCP tool call uses the requesting user's credentials
- Fine-Grained Authorization (FGA) enforces user permissions
- No configuration required - authentication is transparent
```

### 2. AWS RDS Instance Creator README Updates

**File**: `graph-fleet/src/agents/aws_rds_instance_creator/docs/README.md`

**Changes**:

- **Complete Prerequisites Rewrite**: Separated "For Production Use" (no config needed) from "For Local Development" (LLM keys + optional MCP testing)
  - Production: 4 checkmarks emphasizing zero configuration
  - Local: Clear instructions for `.env` setup with optional `PLANTON_API_KEY`

- **Updated MCP Server Section**: Explained automatic authentication in production vs. optional API key locally

- **Enhanced Security Considerations**: Split into Production vs. Local Development subsections
  - Production: Per-user auth, FGA enforcement, audit trail, no shared secrets
  - Local: Test account limitations, restricted permissions

- **Revised Troubleshooting**: Updated authentication troubleshooting to cover both production and local scenarios

**Before/After Example**:

**Before**:
```markdown
### Environment Variables

Create a `.env` file:

```bash
# Required: Your Planton Cloud API key
PLANTON_API_KEY=your_api_key_here
```
```

**After**:
```markdown
### For Production Use

**No additional configuration required!** When using this agent through Planton Cloud:

- ✅ Authentication is automatic (user JWT tokens)
- ✅ Organization and environment context provided automatically
- ✅ MCP tools use your user permissions
- ✅ All actions attributed to your account
```

### 3. Comprehensive Developer Guide (NEW)

**File**: `graph-fleet/docs/DEVELOPER_GUIDE.md` (900+ lines)

Created from scratch to provide complete guidance for custom agent developers.

**Table of Contents**:
1. Introduction (why per-user auth matters)
2. Authentication Architecture (token flow diagram)
3. Creating a New Agent (step-by-step)
4. MCP Tool Integration Pattern (copy-paste examples)
5. Runtime Configuration (how tokens are passed)
6. Testing Your Agent (local, unit tests, staging)
7. Security Best Practices (DO/DON'T with examples)
8. Deployment (local, staging, production)
9. Troubleshooting (common issues and solutions)

**Key Features**:

- **Complete Token Flow Diagram**: ASCII diagram showing user JWT propagation through entire stack
  - Web console → agent-fleet → Temporal → agent-fleet-worker → LangGraph → MCP server → APIs
  - Shows what happens at each layer
  - Explains why token doesn't appear in Temporal history or LangGraph checkpoints

- **Copy-Paste Code Examples**: Working implementations developers can use directly
  ```python
  async def load_mcp_tools(user_token: str) -> Sequence[BaseTool]:
      """Load MCP tools with per-user authentication."""
      if not user_token or not user_token.strip():
          raise ValueError("user_token is required for MCP authentication")
      
      client_config = {
          "planton-cloud": {
              "transport": "streamable_http",
              "url": "https://mcp.planton.ai/",
              "headers": {
                  "Authorization": f"Bearer {user_token}"
              }
          }
      }
      
      mcp_client = MultiServerMCPClient(client_config)
      all_tools = await mcp_client.get_tools()
      
      required_tools = ["get_cloud_resource_schema", "create_cloud_resource"]
      filtered_tools = [t for t in all_tools if t.name in required_tools]
      
      return filtered_tools
  ```

- **Security Best Practices Section**: Detailed DO/DON'T guidance
  - ✅ DO: Always validate tokens (None, empty, whitespace)
  - ✅ DO: Extract token from config, never hardcode
  - ✅ DO: Fail fast with clear error messages
  - ❌ DON'T: Never log or print tokens
  - ❌ DON'T: Never store tokens in agent state
  - ❌ DON'T: Never pass tokens in tool arguments

- **Testing Guidance**: Three-level testing approach
  - Local: LangGraph Studio with test account (single user)
  - Unit Tests: Token validation tests with pytest
  - Staging: Multi-user integration testing with different FGA permissions

- **Troubleshooting Section**: Common issues with causes and solutions
  - "User token not found in config" → How to fix for production vs. local
  - "authentication failed" → Token expiration or invalid credentials
  - "No required tools found" → Tool name mismatches
  - Agent works locally but fails in production → Authentication mechanism differences

### 4. Authentication Architecture Documentation (NEW)

**File**: `graph-fleet/docs/authentication-architecture.md` (800+ lines)

Created comprehensive technical documentation explaining the complete authentication system.

**Table of Contents**:
1. Overview (key principles)
2. Architecture Diagram (complete token flow)
3. Component Details (per-component responsibilities)
4. Before vs. After (static API key vs. per-user auth)
5. Security Benefits (with examples)
6. FGA Enforcement (how it works)
7. Token Lifecycle (timeline from issuance to expiration)
8. Troubleshooting (debugging tips)

**Key Features**:

- **Comprehensive Token Flow Diagram**: Detailed ASCII diagram with all components
  - Shows exact code at each layer
  - Includes Redis storage and retrieval
  - Shows HTTP and gRPC boundaries
  - Explains what data flows where

- **Before/After Comparison**: Visual comparison of old vs. new authentication
  ```
  BEFORE (Static API Key):
  langgraph.json → Static machine account → ALL users share credentials
  ❌ No user attribution
  ❌ FGA bypassed
  
  AFTER (Per-User Auth):
  Runtime config → Per-user JWT token → EACH user has unique credentials
  ✅ Full user attribution
  ✅ FGA enforced
  ```

- **Component-by-Component Details**: Exact responsibilities and code examples for each layer
  - agent-fleet (Java): JWT extraction and Redis storage
  - Temporal: NO token in workflow parameters
  - agent-fleet-worker (Python): Token retrieval and deletion
  - LangGraph agents: Token extraction and MCP client creation
  - MCP server: Authorization header processing
  - Planton APIs: JWT validation and FGA enforcement

- **Security Benefits Explained**: Real-world examples of each benefit
  - User Attribution: Before/after audit log examples
  - FGA Enforcement: Alice (dev) vs. Bob (ops) seeing different resources
  - Principle of Least Privilege: Limited blast radius
  - Token Lifecycle: Timeline from T+0s to T+3600s

- **Token Lifecycle Timeline**: Complete journey with timestamps
  ```
  T+0s     User authenticates to web console
  T+2s     JWT stored in Redis (10-min TTL)
  T+5s     JWT fetched and deleted from Redis
  T+7-60s  Agent executes with JWT in memory
  T+3600s  JWT expires (1-hour lifetime)
  ```

- **Debugging Section**: Step-by-step verification of token flow
  - Check agent-fleet logs: Token stored?
  - Check Redis: Token present?
  - Check agent-fleet-worker logs: Token retrieved?
  - Check LangGraph logs: Token received?
  - Check MCP server logs: Authorization header present?

### 5. Environment Configuration Updates

**File**: `graph-fleet/.env.example`

**Changes**:

Completely reorganized with clear section headers and comments:

```bash
# ========================================
# LLM API Keys (Required)
# ========================================
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# ========================================
# LangSmith Tracing (Optional but Recommended)
# ========================================
LANGSMITH_API_KEY=lsv2_...

# ========================================
# Local Development Only (Optional)
# ========================================
# For testing MCP tools in LangGraph Studio
# Production deployments use automatic per-user authentication
PLANTON_API_KEY=your_test_token_here

# Optional: Override Planton Cloud environment
# PLANTON_CLOUD_ENVIRONMENT=live
```

**Key Improvements**:
- Clear section headers with visual separation
- Explicit "Local Development Only" section for `PLANTON_API_KEY`
- Comment explaining production uses automatic authentication
- Better organization and readability

## Benefits

### For Developers Building Custom Agents

1. **Clear Implementation Path**: Developer Guide provides step-by-step instructions with working code examples
2. **No Guesswork**: All authentication patterns documented with copy-paste examples
3. **Security Confidence**: Understand why per-user auth matters and how to implement it correctly
4. **Faster Onboarding**: New developers can build authenticated agents without reverse-engineering existing code
5. **Better Testing**: Clear guidance on local vs. staging vs. production testing

### For Users of Graph-Fleet Agents

1. **Zero Configuration**: Production usage requires no API keys or manual configuration
2. **Automatic Security**: Per-user authentication happens transparently
3. **Proper Permissions**: Users see only resources they have access to (FGA enforced)
4. **Clear Troubleshooting**: Documentation helps resolve authentication issues quickly

### For System Understanding

1. **Architecture Clarity**: Complete token flow documented with diagrams
2. **Security Model Explained**: Understand how per-user auth protects the system
3. **Component Responsibilities**: Each layer's role clearly documented
4. **Debugging Support**: Step-by-step verification process for troubleshooting

### Documentation Quality Metrics

- **Coverage**: 5 files (3 updated, 2 created)
- **Line Count**: 1,700+ new lines of documentation
- **Code Examples**: 10+ copy-paste code examples
- **Diagrams**: 3 comprehensive ASCII diagrams
- **Troubleshooting Scenarios**: 8+ common issues with solutions
- **Security Guidance**: DO/DON'T lists with 10+ examples

## Impact

### Immediate Impact

**Developer Experience**:
- Developers can now build custom agents with confidence
- No need to reverse-engineer authentication patterns from existing code
- Clear distinction between production (automatic) and local (optional) authentication
- Security best practices well-documented

**User Experience**:
- Clear understanding that production usage requires no configuration
- Troubleshooting guidance for authentication issues
- Confidence in security model (per-user, FGA-enforced)

**Documentation Quality**:
- Outdated static API key references eliminated from production docs
- Comprehensive guides for all audience levels (users, developers, architects)
- Consistent messaging across all documentation

### Long-Term Impact

**Team Velocity**:
- New agent developers onboard faster with comprehensive guides
- Fewer authentication-related bugs due to clear patterns
- Reduced support burden with better troubleshooting documentation

**Security Posture**:
- Developers understand security implications of authentication choices
- Best practices clearly documented and easy to follow
- Security model transparent and auditable

**Maintenance**:
- Documentation accurately reflects implementation (Phases 0-3)
- Future authentication changes have clear documentation to update
- Architecture decisions preserved for future reference

## Related Work

### Previous Phases

This documentation work completes Phase 4 of the 6-phase Dynamic Per-User MCP Authentication project:

- **Phase 0**: Research & Architecture Design
  - Determined solution: HTTP MCP with runtime configuration
  - Documented token flow architecture
  - Created implementation guidance
  - Files: `phase-0-http-mcp-research-findings.md`, `phase-0-architecture-design.md`, `phase-0-security-analysis.md`

- **Phase 1**: Token Storage Infrastructure
  - Implemented Redis-based ephemeral token storage in agent-fleet (Java)
  - User JWT extracted from gRPC metadata
  - Token stored with execution ID as key (10-min TTL)
  - Files: `ExecutionTokenStorageService.java`, `AuthTokenExtractor.java`, `StoreTokenStep.java`
  - Changelog: `2025-11-27-005445-jwt-token-storage-infrastructure.md`

- **Phase 2**: Token Propagation to Worker
  - Implemented token retrieval in agent-fleet-worker (Python)
  - Token fetched from Redis and deleted immediately (one-time use)
  - Token passed to LangGraph via `config["configurable"]["_user_token"]`
  - Files: `execute_langgraph.py` activity
  - Changelog: TBD (Phase 2 completion)

- **Phase 3**: Dynamic MCP Authentication
  - Updated graph-fleet agents to use per-user authentication
  - Implemented `MultiServerMCPClient` with runtime configuration
  - Removed static `mcp_servers` from `langgraph.json`
  - Files: `aws_rds_instance_creator/mcp_tools.py`, `aws_rds_instance_creator/graph.py`
  - Changelog: `2025-11-27-110912-phase-3-dynamic-mcp-authentication.md`

- **Phase 4**: Documentation Updates (this work)
  - Updated all graph-fleet documentation for per-user authentication
  - Created Developer Guide and Authentication Architecture docs
  - Eliminated static API key references from production docs
  - Files: READMEs, `DEVELOPER_GUIDE.md`, `authentication-architecture.md`, `.env.example`

### Next Phases

- **Phase 5**: Comprehensive Testing & Security Validation
  - Multi-user integration tests
  - FGA enforcement verification with different user permissions
  - Security audit (token leakage, replay attacks, Redis security)
  - Load testing with concurrent users
  - Token expiration testing

- **Phase 6**: Documentation & Rollout
  - Operational runbooks for troubleshooting
  - Monitoring dashboards and alerts for token failures
  - Production deployment plan
  - Team training on new authentication model

### GitHub Issue

[#1238: Dynamic Per-User MCP Authentication](https://github.com/plantoncloud-inc/planton-cloud/issues/1238)

## Files Modified

### Updated (3 files)

1. **`graph-fleet/README.md`**
   - Added Authentication section (35 lines)
   - Updated MCP Integration section
   - Enhanced "Adding a New Agent" guidance
   - Changed: ~70 lines

2. **`graph-fleet/src/agents/aws_rds_instance_creator/docs/README.md`**
   - Rewrote Prerequisites section
   - Updated MCP Server documentation
   - Enhanced Security Considerations
   - Revised Troubleshooting section
   - Changed: ~100 lines

3. **`graph-fleet/.env.example`**
   - Reorganized with clear section headers
   - Moved `PLANTON_API_KEY` to "Local Development Only"
   - Added clarifying comments
   - Changed: ~30 lines

### Created (2 files)

4. **`graph-fleet/docs/DEVELOPER_GUIDE.md`** (NEW)
   - Complete guide for building custom agents
   - 900+ lines of documentation
   - 9 major sections covering authentication, implementation, testing, security
   - 10+ copy-paste code examples
   - Comprehensive troubleshooting guide

5. **`graph-fleet/docs/authentication-architecture.md`** (NEW)
   - Technical deep-dive into authentication system
   - 800+ lines of documentation
   - Complete token flow diagrams
   - Component-by-component analysis
   - Before/after security comparison
   - Debugging and troubleshooting guidance

## Design Decisions

### Why Separate Developer Guide from Architecture Docs?

**Decision**: Create two separate documents instead of one comprehensive guide

**Rationale**:
- **Different Audiences**: Developers need implementation guidance; architects need system understanding
- **Different Use Cases**: Developer Guide for "how do I build?"; Architecture Doc for "how does it work?"
- **Better Discoverability**: Clear titles make it easy to find the right document
- **Maintainability**: Changes to authentication pattern update Developer Guide; system architecture changes update Architecture Doc

**Trade-off**: Some overlap in content (token flow appears in both), but each optimized for its audience

### Why Update Agent-Specific README vs. Rely on Main README?

**Decision**: Update AWS RDS Instance Creator README in addition to main README

**Rationale**:
- **User Context**: Users reading agent-specific docs need agent-specific guidance
- **Self-Contained**: Agent README should work standalone without requiring main README
- **Consistency**: All documentation should tell the same story about authentication
- **Discoverability**: Users may land on agent docs directly (e.g., from marketplace)

**Trade-off**: Duplication of some content, but better user experience

### Why Emphasize "Production: No Config" vs. "Local: Optional"?

**Decision**: Lead with production (automatic auth) rather than local development (test credentials)

**Rationale**:
- **Primary Use Case**: Most users interact with agents through Planton Cloud, not locally
- **Security First**: Emphasizing automatic per-user auth reinforces security posture
- **Reduces Confusion**: Prevents users from thinking they need API keys in production
- **Better UX**: "It just works" is better than "configure this first"

**Trade-off**: Local developers need to read further to find setup instructions, but this is appropriate (local dev is secondary use case)

### Why Include So Many Code Examples?

**Decision**: Provide 10+ copy-paste code examples in Developer Guide

**Rationale**:
- **Learning by Example**: Developers understand patterns better with working code
- **Reduce Errors**: Copy-paste examples prevent authentication implementation mistakes
- **Speed**: Faster than reverse-engineering from existing agents
- **Consistency**: Everyone uses the same proven patterns

**Trade-off**: More documentation to maintain when APIs change, but examples are versioned with implementation

## Testing

### Documentation Verification

- ✅ All code examples syntax-checked against actual implementation
- ✅ Token flow diagrams verified against Phase 0-3 implementation
- ✅ Links tested (internal references and external URLs)
- ✅ Markdown formatting validated
- ✅ Consistency checked across all updated files

### Content Review Checklist

- ✅ No references to required static API keys in production documentation
- ✅ Local development clearly marked as optional
- ✅ Production authentication clearly marked as automatic
- ✅ Security best practices DO/DON'T lists comprehensive
- ✅ Troubleshooting covers common scenarios
- ✅ Code examples match actual implementation patterns
- ✅ Token flow diagrams accurate and complete
- ✅ No sensitive information (credentials, private URLs) in examples

## Known Limitations

1. **Examples Use Python**: All code examples are Python (LangGraph agents)
   - Other language implementations (if any) not covered
   - Appropriate since graph-fleet is Python-based

2. **HTTP MCP Only**: Documentation assumes HTTP MCP transport
   - Subprocess/stdio MCP patterns not documented
   - Appropriate since production uses HTTP MCP at `https://mcp.planton.ai/`

3. **Single MCP Server**: Examples focus on single Planton Cloud MCP server
   - Multi-MCP-server authentication not covered
   - Future enhancement if needed

4. **No Video/Visual Diagrams**: All diagrams are ASCII/text-based
   - No rendered architecture diagrams or videos
   - Text-based approach ensures version control and easy updates

## Future Enhancements

1. **Interactive Examples**: Create runnable example agent in separate repository
2. **Video Walkthrough**: Record screencast of building a custom agent
3. **Visual Diagrams**: Create rendered architecture diagrams (Mermaid, etc.)
4. **Multi-Language Support**: If graph-fleet expands beyond Python, add language-specific guidance
5. **Testing Templates**: Provide pytest templates for common authentication test scenarios
6. **IDE Integration**: Create code snippets/templates for VSCode, IntelliJ

## Success Criteria

### Phase 4 Goals (All Achieved)

- ✅ All references to required `PLANTON_API_KEY` removed from production docs
- ✅ Local development scenarios clearly documented as optional
- ✅ Developer guide provides copy-paste code examples
- ✅ Authentication architecture clearly explained
- ✅ Security best practices documented
- ✅ Multi-user testing guidance provided
- ✅ No breaking changes for existing local development workflows
- ✅ Documentation is consistent across all files

### Verification

- ✅ User searching for "PLANTON_API_KEY required" finds clear guidance
- ✅ Developer building custom agent can follow Developer Guide without gaps
- ✅ Architect understanding system can read Architecture Doc and comprehend token flow
- ✅ Support engineer troubleshooting auth issue has debugging guidance
- ✅ Security reviewer auditing system can verify per-user authentication model

---

**Status**: ✅ Phase 4 Complete  
**Timeline**: Phase 4 documentation completed in ~4 hours  
**Next Phase**: Phase 5 - Comprehensive Testing & Security Validation  
**Impact**: **High** - Enables developer adoption of per-user authentication patterns


