# Demo Scenarios - AWS RDS Manifest Generator

Compelling demonstration scripts for showcasing the AWS RDS Manifest Generator agent.

## Table of Contents

- [Scenario 1: Speed Run (2 minutes)](#scenario-1-speed-run-2-minutes)
- [Scenario 2: Conversational Mastery (5 minutes)](#scenario-2-conversational-mastery-5-minutes)
- [Scenario 3: Full Feature Demo (8 minutes)](#scenario-3-full-feature-demo-8-minutes)
- [Key Talking Points](#key-talking-points)
- [Expected Questions & Answers](#expected-questions--answers)
- [Demo Setup Checklist](#demo-setup-checklist)

## Scenario 1: Speed Run (2 minutes)

**Goal**: Demonstrate the fastest path from request to manifest

**Audience**: Technical decision makers, founders

**Key Message**: "Creating AWS infrastructure manifests is now as simple as having a conversation"

### Setup

- LangGraph Studio running on http://localhost:8123
- `rds_manifest_generator` graph selected
- Clean conversation state

### Script

**[0:00] Introduction (15 seconds)**

> "Let me show you how we're revolutionizing infrastructure-as-code. Instead of wrestling with YAML syntax and AWS documentation, you just describe what you need in plain English. Watch this."

**[0:15] The Request (5 seconds)**

*Type in chat:*
```
I need a production Postgres database for my API backend
```

**[0:20] Agent Planning (10 seconds)**

*Agent creates visible todo plan:*
```
Creating AWS RDS manifest for production Postgres:
1. Database configuration ⏳
2. Instance sizing ⏳
3. Credentials ⏳
4. Network configuration ⏳
5. High availability options ⏳
```

> "Notice how the agent immediately creates a plan. It knows what information it needs and shows you the roadmap."

**[0:30] Intelligent Questions (45 seconds)**

*Agent asks:*
```
What Postgres version would you like? For production, I'd recommend 14.10 or 15.5.
```

*You answer:*
```
15.5
```

*Agent:*
```
Perfect! What instance size? For production APIs I recommend:
- db.m6g.large for medium traffic
- db.m6g.xlarge for high traffic
```

*You:*
```
db.m6g.large, 100 GB storage, username dbadmin, password temp123
```

> "See how the agent provides context and recommendations? It's not just collecting data—it's educating and guiding based on AWS best practices."

*Agent:*
```
For production I recommend Multi-AZ deployment and storage encryption. Enable both?
```

*You:*
```
Yes
```

*Agent:*
```
Network configuration - subnet IDs? (Need at least 2 for Multi-AZ)
```

*You:*
```
subnet-1a, subnet-1b, security group sg-api-db
```

**[1:15] The Magic Moment (30 seconds)**

*Agent validates and generates:*
```yaml
apiVersion: aws.project-planton.org/v1
kind: AwsRdsInstance
metadata:
  name: postgres-instance-k7m2x9
  org: project-planton
  env: aws
spec:
  engine: postgres
  engineVersion: "15.5"
  instanceClass: db.m6g.large
  allocatedStorageGb: 100
  username: dbadmin
  password: temp123
  multiAz: true
  storageEncrypted: true
  subnetIds:
    - subnet-1a
    - subnet-1b
  securityGroupIds:
    - sg-api-db
```

> "And there it is—a complete, production-ready AWS RDS manifest in under 2 minutes. Proper YAML structure, camelCase field names, validation built in."

**[1:45] The Punchline (15 seconds)**

> "This agent understands the AWS RDS protobuf schema. No hardcoded templates. No manual YAML writing. And here's the kicker—this exact approach works for all 30+ AWS resource types in our platform. Same conversation, different resources."

### Key Highlights for Speed Run

- **Time to value**: Under 2 minutes
- **Zero YAML knowledge** required
- **AI-driven questions**: No templates needed
- **Production-ready output**: Multi-AZ, encrypted, validated
- **Scalability**: Same approach for 30+ resource types

---

## Scenario 2: Conversational Mastery (5 minutes)

**Goal**: Show the agent's intelligence in handling vague requests

**Audience**: Engineering teams, product managers

**Key Message**: "The agent doesn't just collect data—it understands context and guides you to the right solution"

### Setup

Same as Scenario 1

### Script

**[0:00] Introduction (20 seconds)**

> "Most infrastructure tools force you to know exactly what you want upfront. That's not how humans think. Let me show you an agent that works the way you actually talk about infrastructure."

**[0:20] Deliberately Vague Request (5 seconds)**

*Type:*
```
I need a database for production
```

**[0:25] Agent Extracts Context (30 seconds)**

*Agent:*
```
I'll help you create a production database! A few questions to get started:

1. What database engine do you prefer?
   - PostgreSQL (great for general purpose, strong ACID compliance)
   - MySQL (popular, good ecosystem)
   - MariaDB (MySQL fork, community-driven)
   - Oracle (enterprise features, licensing required)
   - SQL Server (Microsoft ecosystem)

What fits your tech stack?
```

> "Notice it's not just asking 'what engine?' It's providing context about each option. The agent combines schema knowledge with AWS expertise from its training."

*You:*
```
We're a startup using Node.js and Python, what do you recommend?
```

*Agent:*
```
For a Node.js/Python stack, I'd strongly recommend PostgreSQL. It has:
- Excellent drivers for both ecosystems
- Strong JSON support (great for modern APIs)
- ACID compliance for data integrity
- Active community and tooling

Shall we go with Postgres?
```

> "See that? It didn't just list options—it made a recommendation based on your context."

**[0:55] Handling Unclear Responses (1 minute)**

*You:*
```
Sure. Make it fast and not too expensive.
```

*Agent:*
```
Got it—balancing performance and cost! For production Postgres, I recommend:

Instance: db.t3.small
- 2 vCPUs, 2 GB RAM
- Cost-effective for low-medium traffic
- Easy to scale up later
- ~$25/month for single-AZ

Storage: Start with 50 GB
- Enough for most early-stage apps
- Auto-scales if needed

Does this align with your expected traffic? How many users/requests are you planning for?
```

*You:*
```
Maybe 100-500 concurrent users at peak
```

*Agent:*
```
For 500 concurrent users, t3.small might struggle during peak times. Let me adjust:

Instance: db.m6g.large
- Better for your traffic pattern
- 2 vCPUs, 8 GB RAM
- Handles concurrent connections well
- ~$140/month single-AZ, ~$280/month Multi-AZ

For production, I'd also recommend Multi-AZ deployment for 99.95% availability. Your users won't appreciate downtime. Sound good?
```

> "The agent is doing something remarkable here—it's translating business requirements into technical specifications. From 'not too expensive' and '500 users' to specific instance recommendations."

**[1:55] Soft Validation Example (1 minute)**

*You:*
```
OK, use m6g.large, but keep it cheap so skip Multi-AZ
```

*Agent:*
```
I can do that, but let me make sure you're aware of the tradeoff:

Without Multi-AZ:
✓ Cost: ~$140/month (saves $140)
✗ Availability: ~99.5% (could be down ~3.6 hours/month)
✗ No automatic failover
✗ Downtime during maintenance

With Multi-AZ:
✓ Availability: 99.95% (~22 minutes downtime/month)
✓ Automatic failover if primary fails
✓ Zero-downtime maintenance
✗ Cost: ~$280/month

For production with 500 users, Multi-AZ is usually worth it. But it's your call—should I enable it or keep costs down?
```

*You:*
```
You're right, let's do Multi-AZ
```

> "This is soft validation in action. The agent isn't blocking the user—it's educating them about consequences. Then it lets them make the informed decision."

**[2:55] Handling Invalid Input (1 minute)**

*You:*
```
Instance class is m6g.large, username admin, password pass, storage 100
```

*Agent:*
```
Almost there! Just a couple of adjustments:

1. Instance class needs to be "db.m6g.large" (must start with "db.")
2. Password "pass" is very weak. For production, use at least 8 characters with mixed case, numbers, and symbols.
3. For storage, I've got 100 GB ✓

Shall I use:
- Instance: db.m6g.large
- Username: admin
- Password: (please provide a stronger one)
- Storage: 100 GB
```

*You:*
```
db.m6g.large, admin, TempPass123!, 100GB
```

*Agent:*
```
Perfect! Got it:
- Instance: db.m6g.large ✓
- Username: admin ✓
- Password: TempPass123! ✓ (remember to rotate this with proper secrets management)
- Storage: 100 GB ✓
```

> "The agent validates using proto validation rules, but explains errors conversationally. No cryptic error messages."

**[3:55] Network Configuration (45 seconds)**

*Agent:*
```
Last piece—network configuration. I need:
1. Subnet IDs (at least 2 for Multi-AZ, in different availability zones)
2. Security group IDs (controls which resources can connect)

Do you have these, or would you like guidance on finding them?
```

*You:*
```
I'm not sure, can I use placeholders for now?
```

*Agent:*
```
Absolutely! For testing the manifest generation, you can use placeholders like:
- subnet-placeholder-1a
- subnet-placeholder-2b
- sg-placeholder-db

You'll need to update these with real AWS resource IDs before deployment. Should I use these placeholders?
```

*You:*
```
Yes
```

**[4:40] Manifest Generation (20 seconds)**

*Agent generates complete manifest*

> "And there we have it. From 'I need a database' to a complete, production-ready manifest. The agent extracted requirements through conversation, provided recommendations, validated inputs, and educated the user along the way."

### Key Highlights for Conversational Mastery

- **Vague to specific**: Handles unclear requests gracefully
- **Context-aware**: Recommendations based on use case
- **Educational**: Explains tradeoffs and consequences
- **Soft validation**: Guides instead of blocking
- **Flexible**: Accepts placeholders, handles various input formats
- **Conversational**: Natural back-and-forth, not rigid forms

---

## Scenario 3: Full Feature Demo (8 minutes)

**Goal**: Demonstrate all capabilities comprehensively

**Audience**: Technical teams, potential integrators, investors

**Key Message**: "This is a complete, production-ready AI agent with deep AWS knowledge and intelligent workflows"

### Setup

Same as previous scenarios

### Script

**[0:00] Introduction (30 seconds)**

> "I'm going to give you a comprehensive tour of the AWS RDS Manifest Generator. We'll see schema querying, requirement validation, metadata handling, and the complete workflow from conversation to deployment-ready YAML. This demonstrates the full power of AI-native infrastructure tooling."

**[0:30] Schema Understanding Demo (1 minute 30 seconds)**

*Type:*
```
Before we start, can you tell me what fields are required for an RDS instance?
```

*Agent uses `list_required_fields()`:*
```
Required fields for AWS RDS Instance:
- engine: Database engine type (postgres, mysql, mariadb, oracle-se2, sqlserver-ex, etc.)
- engine_version: Specific version of the database engine
- instance_class: EC2 instance type (must start with "db.")
- allocated_storage_gb: Storage size in GB (must be > 0)
- username: Master database username (minimum length varies by engine)
- password: Master database password
- subnet_ids: VPC subnet IDs for deployment (need at least 2 for Multi-AZ)
- security_group_ids: Security group IDs for access control
```

*You:*
```
What about optional fields?
```

*Agent uses `list_optional_fields()`:*
```
Optional fields you can configure:
- multi_az: Enable Multi-AZ deployment (boolean)
- storage_encrypted: Enable encryption at rest (boolean)
- kms_key_id: Custom KMS key for encryption (string)
- port: Database port (integer, 0-65535)
- publicly_accessible: Assign public IP (boolean)
- parameter_group_name: Custom parameter group
- option_group_name: Custom option group
- db_subnet_group_name: Existing subnet group to use
[... more fields ...]
```

> "The agent is reading this directly from the AWS RDS protobuf schema. It's not hardcoded—it's dynamically understood. Now watch this:"

*You:*
```
Tell me more about the instance_class field
```

*Agent uses `get_rds_field_info('instance_class')`:*
```
Field: instance_class
Type: string
Required: Yes
Description: The compute and memory capacity of the DB instance. Instance classes comprise varying combinations of CPU, memory, and storage capacity.

Validation Rules:
- Must start with "db." (pattern: ^db\\.*)
- Minimum length: 1 character

Examples:
- db.t3.micro (1 vCPU, 1 GB RAM) - Dev/test
- db.m6g.large (2 vCPU, 8 GB RAM) - General purpose
- db.r6g.xlarge (4 vCPU, 32 GB RAM) - Memory optimized
```

> "This is how the agent knows what to ask and how to validate. It queries the schema on demand, combining that with its AWS knowledge to generate intelligent questions."

**[2:00] Complex Requirements Collection (3 minutes)**

*You:*
```
I want to create a highly available MariaDB instance called "production-analytics-db" for our data analytics platform. Tag it with team=data-engineering and environment=production.
```

*Agent uses `set_manifest_metadata()`:*
```
Perfect! I'll create a manifest named "production-analytics-db" with those labels.

[Creates comprehensive todo plan]

Let's configure your production MariaDB instance...
```

> "Notice it extracted the resource name and labels from the natural language request. It's parsing intent, not just collecting form data."

*[Conversation proceeds through all fields, with agent providing context and recommendations for each]*

*At the midpoint:*

*You:*
```
What have we configured so far?
```

*Agent uses `get_collected_requirements()`:*
```
Here's what we've configured so far:

✓ Database Configuration:
  - engine: mariadb
  - engineVersion: "10.11"
  
✓ Instance Sizing:
  - instanceClass: db.r6g.xlarge
  - allocatedStorageGb: 500
  
✓ Credentials:
  - username: mariadb_admin
  - password: [configured]
  
✓ High Availability:
  - multiAz: true
  - storageEncrypted: true
  
⏳ Still needed:
  - Network configuration (subnets, security groups)
```

> "The agent can review progress at any time. It's tracking everything in memory."

**[5:00] Validation Before Generation (1 minute)**

*After collecting all information:*

*You:*
```
Before you generate the manifest, can you validate everything?
```

*Agent uses `validate_manifest()`:*
```
Running validation checks...

✓ All required fields present
✓ engine: "mariadb" is valid
✓ engine_version: "10.11" meets constraints (min_len: 1)
✓ instance_class: "db.r6g.xlarge" matches pattern ^db\\.
✓ allocated_storage_gb: 500 is > 0
✓ username: "mariadb_admin" meets constraints
✓ password: configured and valid
✓ subnet_ids: 3 subnets provided (min 2 for Multi-AZ)
✓ security_group_ids: 2 security groups configured

All requirements are valid and complete! Ready to generate manifest.
```

> "This is validating against the same proto validation rules that will be enforced when you deploy. No surprises later."

**[6:00] Manifest Generation (1 minute)**

*Agent uses `generate_rds_manifest(resource_name='production-analytics-db')`:*

```yaml
apiVersion: aws.project-planton.org/v1
kind: AwsRdsInstance
metadata:
  name: production-analytics-db
  org: project-planton
  env: aws
  labels:
    team: data-engineering
    environment: production
spec:
  engine: mariadb
  engineVersion: "10.11"
  instanceClass: db.r6g.xlarge
  allocatedStorageGb: 500
  username: mariadb_admin
  password: secure-password-rotate-me
  port: 3306
  publiclyAccessible: false
  multiAz: true
  storageEncrypted: true
  kmsKeyId: arn:aws:kms:us-east-1:123456789012:key/custom-key-id
  subnetIds:
    - subnet-prod-1a
    - subnet-prod-1b
    - subnet-prod-1c
  securityGroupIds:
    - sg-mariadb-prod
    - sg-analytics-access
  parameterGroupName: custom-mariadb-params
  optionGroupName: custom-mariadb-options
```

*Agent explains:*
```
Here's your production-ready MariaDB manifest with enterprise features:

Architecture:
- Multi-AZ deployment across 3 availability zones
- Memory-optimized instance (db.r6g.xlarge: 4 vCPU, 32 GB RAM)
- 500 GB encrypted storage with custom KMS key

Security:
- Private network access only (publiclyAccessible: false)
- Two-layer security groups (production isolation + analytics access)
- Encrypted at rest with custom KMS key

Customization:
- Custom parameter group for performance tuning
- Custom option group for additional features

Labels:
- team: data-engineering (for cost allocation)
- environment: production (for resource organization)

You can save this to production-analytics-db.yaml and deploy with:
planton apply -f production-analytics-db.yaml
```

**[7:00] Demonstration of Flexibility (1 minute)**

*You:*
```
Actually, I want to change the storage to 1000 GB
```

*Agent:*
```
No problem! Let me regenerate with 1000 GB storage...

[Updates requirement and generates new manifest]

Updated! Your manifest now shows:
  allocatedStorageGb: 1000

Everything else remains the same. Want any other changes?
```

*You:*
```
Can you regenerate this for a dev environment instead?
```

*Agent:*
```
I can help you create a dev version! Should I:
1. Keep the same configuration but change labels/name?
2. Scale down to dev-appropriate resources (smaller instance, single-AZ)?

What makes sense for your dev environment?
```

> "The agent is flexible. You can update individual fields, regenerate with changes, or even create variations for different environments."

### Key Highlights for Full Feature Demo

- **Schema Querying**: Live proto parsing and field information
- **Metadata Handling**: Names and labels from natural language
- **Progress Tracking**: Review collected requirements anytime
- **Validation**: Pre-generation validation against proto rules
- **Field Conversion**: Automatic snake_case → camelCase
- **Comprehensive Output**: All fields properly formatted
- **Flexibility**: Easy updates and regeneration
- **Intelligence**: Context-aware recommendations throughout

---

## Key Talking Points

### For Technical Audiences

1. **No Templates Required**
   - "Every question is generated dynamically from the proto schema"
   - "Add a new field to the proto? The agent automatically asks about it"
   - "This scales to all 30+ AWS resource types with zero code changes"

2. **Proto-Driven Architecture**
   - "Single source of truth: the protobuf schema"
   - "Validation rules come directly from buf.validate annotations"
   - "Same approach works for any proto-defined resource"

3. **AI-Native Design**
   - "Combines schema knowledge with AWS best practices from training data"
   - "Not just form filling—intelligent guidance and recommendations"
   - "Learns from conversation context to provide relevant suggestions"

### For Business Audiences

1. **Time Savings**
   - "From hours of YAML wrestling to minutes of conversation"
   - "Reduces infrastructure setup from a specialized skill to a conversation"
   - "Engineers can focus on building features, not fighting config files"

2. **Reduced Errors**
   - "Validation happens during conversation, not at deployment"
   - "Agent guides users away from common mistakes"
   - "Production best practices built in (Multi-AZ, encryption, etc.)"

3. **Scalability**
   - "This demo is one resource type—we have 30+"
   - "Same conversation interface for S3, ECS, Lambda, RDS, etc."
   - "One platform for all infrastructure needs"

### For Investors

1. **Technology Moat**
   - "Proto-driven architecture is unique and defensible"
   - "AI agents that understand infrastructure schemas"
   - "Scales across cloud providers and resource types"

2. **Market Opportunity**
   - "Infrastructure-as-code is a $10B+ market"
   - "Every company needs infrastructure, but most struggle with complexity"
   - "We're making infrastructure accessible to 10x more developers"

3. **Vision**
   - "This is infrastructure's ChatGPT moment"
   - "From code to conversation"
   - "The future of how teams manage cloud resources"

---

## Expected Questions & Answers

### Q: "What if I don't know the AWS subnet IDs?"

**A**: "Great question! The agent is flexible. You can:
1. Use placeholders for testing the manifest generation
2. Ask the agent for guidance on finding them (it can explain AWS console steps)
3. In production, our platform will auto-inject these from your configured AWS environment

The agent works at the proof-of-concept level now, but we're building platform integration for seamless AWS resource discovery."

### Q: "Can it handle multiple databases in one conversation?"

**A**: "Currently each conversation generates one manifest. For multiple resources, you'd have separate conversations. 

However, that's actually a feature request in our backlog—'batch generation.' Imagine: 'Create 5 similar databases for these microservices' and the agent creates all 5 manifests. Totally feasible with our architecture."

### Q: "What about other AWS services like S3 or Lambda?"

**A**: "Excellent question! The beauty of our proto-driven architecture is that it's resource-agnostic. 

See these proto files? [Show schema/protos/] We have similar schemas for S3, ECS, Lambda, and 30+ other resources. Creating a new agent is:
1. Copy the proto files
2. Wire up the schema loader
3. That's it—same tools, same workflow

We chose RDS as the first demo because it's complex enough to showcase the capabilities."

### Q: "How do you ensure the generated YAML is secure?"

**A**: "Security happens at multiple levels:

1. **Validation**: The agent validates against AWS requirements and best practices
2. **Recommendations**: It actively recommends security features (encryption, private networking, Multi-AZ)
3. **Education**: It explains security implications of each choice
4. **Platform Integration**: In production, our platform enforces additional security policies

The agent won't let you accidentally create an insecure database—it'll guide you to best practices."

### Q: "What's the accuracy rate?"

**A**: "Because the agent uses the actual proto schema definitions, accuracy on field types and validations is 100%—it's reading from the source of truth.

For recommendations (like instance sizing), it's using AWS knowledge from Claude's training data, which is very reliable.

The conversational flow might need 1-2 clarifications sometimes, but that's actually a feature—it's confirming rather than assuming."

### Q: "Can I integrate this into our existing tools?"

**A**: "Absolutely! We've designed this as a composable system:

1. **API Integration**: The agent is a LangGraph deployment—you can call it via API
2. **UI Embedding**: Embed the conversation interface in your web app
3. **CLI**: Run it from the command line for automation
4. **Platform Native**: Use it within Planton Cloud

Check out our integration guide [show INTEGRATION.md] for technical details."

### Q: "What about costs? Each question is an LLM call."

**A**: "Great observation! Current costs per manifest generation:
- ~10-20 LLM calls per conversation
- Using Claude Sonnet 4: ~$0.05-0.15 per manifest
- Compare to: Hours of developer time at $50-150/hour

The ROI is clear. Plus, we're working on optimizations:
- Caching common questions
- Batch validation
- Cheaper models for simple tasks

We expect to get this under $0.01 per manifest at scale."

---

## Demo Setup Checklist

### Before the Demo

- [ ] LangGraph Studio running (`make run`)
- [ ] Browser open to http://localhost:8123
- [ ] `rds_manifest_generator` graph selected
- [ ] ANTHROPIC_API_KEY environment variable set
- [ ] Test a quick conversation to ensure it's working
- [ ] Have proto files ready to show if asked
- [ ] Have code editor open to show architecture if needed
- [ ] Close unnecessary browser tabs/applications
- [ ] Turn off notifications

### During the Demo

- [ ] Start with a clean conversation
- [ ] Type clearly and deliberately (so audience can follow)
- [ ] Pause after key moments to let them absorb
- [ ] Show the todo plan updates
- [ ] Highlight tool calls in LangGraph Studio UI if technical audience
- [ ] Copy/paste the final YAML into a file to show it's real

### After the Demo

- [ ] Ask "What questions do you have?"
- [ ] Offer to demo specific scenarios they're interested in
- [ ] Share documentation links
- [ ] Collect feedback on what resonated
- [ ] Note any questions you couldn't answer

### Backup Plans

**If internet is slow:**
- Pre-record a demo video as backup
- Use faster model if available

**If agent gives unexpected response:**
- "That's actually interesting—the agent is reasoning through..."
- Acknowledge and pivot to a new conversation
- Have a second browser window ready with working conversation

**If technical issues:**
- Have screenshots of successful runs ready
- Walk through the generated YAML from a file
- Focus on architecture discussion instead of live demo

---

## Customizing for Your Audience

### For Engineering Teams
- Emphasize schema querying and validation
- Show the code structure
- Demonstrate debugging in LangGraph Studio
- Discuss extensibility and integration

### For Product Teams
- Focus on user experience
- Emphasize time savings
- Show conversational intelligence
- Discuss future features

### For Executives
- Quick speed run demonstration
- Focus on business value and ROI
- Emphasize scalability story
- Discuss market opportunity

### For Investors
- Vision and technology moat
- Market size and opportunity
- Demonstration of capabilities
- Roadmap and scale plan

---

**Remember**: The goal isn't to show every feature—it's to tell a compelling story about how AI is transforming infrastructure management. Choose the scenario that best resonates with your audience and practice it until it feels natural.

