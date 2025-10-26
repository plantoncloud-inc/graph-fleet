# User Guide - AWS RDS Manifest Generator

A comprehensive guide to using the AWS RDS Manifest Generator agent.

## Table of Contents

- [Getting Started](#getting-started)
- [Example Conversations](#example-conversations)
- [Understanding the Workflow](#understanding-the-workflow)
- [Field Reference](#field-reference)
- [Tips & Tricks](#tips--tricks)
- [Troubleshooting](#troubleshooting)

## Getting Started

### What Is This?

The AWS RDS Manifest Generator is an AI agent that helps you create AWS RDS Instance YAML manifests through natural language conversation. Instead of learning complex YAML syntax and AWS RDS configuration options, you just describe what you need in plain English.

### How to Access

1. Navigate to the project directory
2. Run `make run` to start LangGraph Studio
3. Open http://localhost:8123 in your browser
4. Select the `rds_manifest_generator` graph
5. Start chatting!

### Your First Interaction

Try this simple request:

```
I need a PostgreSQL database for my application
```

The agent will guide you through the entire process with intelligent questions.

## Example Conversations

### Scenario 1: Production Postgres for API

**Goal**: Create a production-ready Postgres database for a REST API

```
You: I want to create a production Postgres database for my API backend

Agent: Great! I'll help you create an AWS RDS Instance manifest for a production Postgres database.
       Let me gather the necessary information.
       
       [Creates plan showing: Database Config, Instance Sizing, Credentials, Network, HA Options]
       
       What Postgres version would you like to use? For production, I'd recommend:
       - 14.10 (stable, widely tested)
       - 15.5 (newer features, good performance)

You: 15.5 sounds good

Agent: Perfect! Postgres 15.5 is an excellent choice.
       
       Now, what instance size do you need? This depends on your expected workload:
       - db.t3.micro - Dev/test only, very limited resources
       - db.t3.small - Light production workloads
       - db.m6g.large - Medium production (recommended for most APIs)
       - db.m6g.xlarge - High-traffic production
       - db.r6g.large+ - Memory-intensive workloads
       
       What's your expected traffic volume?

You: Medium traffic, maybe 1000-5000 requests per minute

Agent: For that traffic level, db.m6g.large is perfect. It provides:
       - 2 vCPUs
       - 8 GB RAM
       - Good balance of compute and memory
       
       How much storage do you need in GB?

You: 100 GB

Agent: Great! 100 GB gives you room to grow.
       
       What username should I set for the master database user?

You: dbadmin

Agent: And the password? (This will be stored in the manifest, so you'll want to 
       replace it with a secure credential later)

You: temp-password-123

Agent: Got it. For production, I'd recommend enabling some important features:
       
       1. Multi-AZ deployment - Provides automatic failover to a standby instance in 
          another availability zone. Recommended for production. Enable this?

You: Yes

Agent: Excellent choice for high availability.
       
       2. Storage encryption - Encrypts your data at rest using AWS KMS. Recommended 
          for production. Enable this?

You: Yes

Agent: Great! Now I need some network configuration.
       
       What subnet IDs should this RDS instance use? You'll need at least 2 subnets 
       in different availability zones. (Example: subnet-abc123, subnet-def456)

You: subnet-12345, subnet-67890

Agent: Perfect. What security group IDs should control access to this database?
       (Example: sg-abc123)

You: sg-production-db

Agent: Excellent! I have all the required information. Let me validate and generate 
       your manifest...
       
       [Validates requirements]
       
       Here's your AWS RDS Instance manifest:

```yaml
apiVersion: aws.project-planton.org/v1
kind: AwsRdsInstance
metadata:
  name: postgres-instance-x7k2p9
  org: project-planton
  env: aws
spec:
  engine: postgres
  engineVersion: "15.5"
  instanceClass: db.m6g.large
  allocatedStorageGb: 100
  username: dbadmin
  password: temp-password-123
  multiAz: true
  storageEncrypted: true
  subnetIds:
    - subnet-12345
    - subnet-67890
  securityGroupIds:
    - sg-production-db
```

This configures a production-ready Postgres 15.5 database with:
- Multi-AZ deployment for 99.95% availability
- 100 GB of encrypted storage
- db.m6g.large instance (2 vCPU, 8 GB RAM)
- Deployed across multiple availability zones
- Proper security group isolation

You can save this to `rds-instance.yaml` and deploy with:
`planton apply -f rds-instance.yaml`

Would you like to make any changes?
```

### Scenario 2: Development MySQL Instance

**Goal**: Simple MySQL database for local development testing

```
You: I need a small MySQL database for development

Agent: I'll help you create a development MySQL RDS instance.
       
       [Creates plan]
       
       What MySQL version would you like? Popular options:
       - 8.0 (latest, recommended)
       - 5.7 (older, but stable)

You: 8.0

Agent: Great! For development, what instance size?
       - db.t3.micro - Cheapest option, fine for dev
       - db.t3.small - A bit more power

You: db.t3.micro is fine

Agent: Perfect for dev! How much storage? Even 20 GB is plenty for development.

You: 20 GB

Agent: What username for the database?

You: devuser

Agent: And a password? (Remember, this is just for dev)

You: devpass123

Agent: For development, you probably don't need Multi-AZ or encryption to save costs.
       Should I keep this simple?

You: Yes, keep it simple

Agent: I'll need subnet IDs and security groups. Do you have those?

You: subnet-dev-1, subnet-dev-2, and sg-dev-db

Agent: Perfect! Generating your development manifest...

```yaml
apiVersion: aws.project-planton.org/v1
kind: AwsRdsInstance
metadata:
  name: mysql-instance-dev-a3b9c1
  org: project-planton
  env: aws
spec:
  engine: mysql
  engineVersion: "8.0"
  instanceClass: db.t3.micro
  allocatedStorageGb: 20
  username: devuser
  password: devpass123
  subnetIds:
    - subnet-dev-1
    - subnet-dev-2
  securityGroupIds:
    - sg-dev-db
```

This is a minimal development configuration - no Multi-AZ, no encryption, small instance.
Perfect for testing and development work!
```

### Scenario 3: High-Availability MariaDB

**Goal**: Enterprise-grade MariaDB with all production features

```
You: I need a highly available MariaDB database with all production features

Agent: I'll help you create an enterprise-grade MariaDB instance with HA features.
       
       [Creates comprehensive plan]
       
       What MariaDB version? I'd recommend 10.11 (latest stable).

You: 10.11

Agent: For high availability, I recommend db.r6g.xlarge or larger. These are memory-optimized.
       What's your workload like?

You: Heavy read/write traffic, needs lots of memory

Agent: Perfect, let's go with db.r6g.xlarge:
       - 4 vCPUs
       - 32 GB RAM
       - Optimized for database workloads

You: Sounds good

Agent: How much storage? For enterprise, I'd suggest 500 GB or more.

You: Let's do 1000 GB

Agent: Excellent - that gives you plenty of headroom.
       
       Username for master user?

You: mariadb_admin

Agent: Password? (You'll rotate this with proper secrets management)

You: initial-password-rotate-me

Agent: For high availability, I'll enable:
       - Multi-AZ deployment (automatic failover)
       - Storage encryption
       - Backup retention
       
       What port should MariaDB listen on? Default is 3306.

You: Use the default

Agent: Should this database be publicly accessible? (Not recommended for security)

You: No, keep it private

Agent: Good security practice! 
       
       Subnet IDs for deployment? (Need at least 2 for Multi-AZ)

You: subnet-prod-a, subnet-prod-b, subnet-prod-c

Agent: Security group IDs?

You: sg-mariadb-prod, sg-app-access

Agent: Excellent! Let me generate your enterprise-grade manifest...

```yaml
apiVersion: aws.project-planton.org/v1
kind: AwsRdsInstance
metadata:
  name: mariadb-ha-instance-p9x4k2
  org: project-planton
  env: aws
spec:
  engine: mariadb
  engineVersion: "10.11"
  instanceClass: db.r6g.xlarge
  allocatedStorageGb: 1000
  username: mariadb_admin
  password: initial-password-rotate-me
  port: 3306
  publiclyAccessible: false
  multiAz: true
  storageEncrypted: true
  subnetIds:
    - subnet-prod-a
    - subnet-prod-b
    - subnet-prod-c
  securityGroupIds:
    - sg-mariadb-prod
    - sg-app-access
```

This is an enterprise-grade configuration with:
- Multi-AZ for 99.95% availability SLA
- 1 TB encrypted storage
- Memory-optimized instance (32 GB RAM)
- Private network access only
- Multiple security groups for layered security

Ready for mission-critical production workloads!
```

### Scenario 4: Oracle Database for Testing

**Goal**: Basic Oracle database for application testing

```
You: I need an Oracle database for testing our application

Agent: I'll help you create an Oracle RDS instance.
       
       What Oracle edition? AWS RDS supports:
       - oracle-se2 (Standard Edition 2)
       - oracle-ee (Enterprise Edition)

You: Standard Edition 2 is fine

Agent: What version? For example, 19.0.0.0 is common.

You: 19.0.0.0

Agent: For testing, what size instance?

You: Something small, maybe db.t3.small

Agent: Good for testing! How much storage?

You: 50 GB

Agent: Master username? (Note: Oracle has specific username requirements)

You: oracleadmin

Agent: Password?

You: Test123456

Agent: Network configuration - subnet IDs?

You: subnet-test-1, subnet-test-2

Agent: Security group?

You: sg-oracle-test

Agent: Here's your Oracle test instance:

```yaml
apiVersion: aws.project-planton.org/v1
kind: AwsRdsInstance
metadata:
  name: oracle-se2-instance-t5n8m3
  org: project-planton
  env: aws
spec:
  engine: oracle-se2
  engineVersion: "19.0.0.0"
  instanceClass: db.t3.small
  allocatedStorageGb: 50
  username: oracleadmin
  password: Test123456
  subnetIds:
    - subnet-test-1
    - subnet-test-2
  securityGroupIds:
    - sg-oracle-test
```

A basic Oracle SE2 instance ready for application testing!
```

## Understanding the Workflow

### Phase 1: Planning

When you make a request, the agent creates a visible plan showing what information it needs to collect. This helps you understand what to expect.

### Phase 2: Information Gathering

The agent asks intelligent questions based on:
- The AWS RDS protobuf schema (for requirements and validation rules)
- AWS best practices (from its training data)
- Your use case (production vs development, etc.)

### Phase 3: Validation

As you provide answers, the agent validates them against proto validation rules:
- Pattern matching (e.g., instance_class must start with "db.")
- Numeric constraints (e.g., storage must be > 0)
- String length requirements

If something doesn't validate, it explains the issue conversationally and asks again.

### Phase 4: Manifest Generation

Once all required information is collected, the agent:
1. Validates all requirements
2. Converts field names from snake_case to camelCase
3. Builds the complete YAML structure
4. Presents the manifest with explanations

## Field Reference

### Required Fields

**engine**
- What: Database engine type
- Values: `postgres`, `mysql`, `mariadb`, `oracle-se2`, `oracle-ee`, `sqlserver-ex`, `sqlserver-se`, `sqlserver-web`, `sqlserver-ee`
- Example: `postgres`

**engineVersion**
- What: Specific version of the database engine
- Format: Version string (e.g., "15.5", "8.0", "10.11")
- Example: `"15.5"` for Postgres

**instanceClass**
- What: EC2 instance type for the database
- Pattern: Must start with "db."
- Examples: 
  - `db.t3.micro` - Dev/test (1 vCPU, 1 GB RAM)
  - `db.t3.small` - Light workloads (2 vCPU, 2 GB RAM)
  - `db.m6g.large` - General purpose (2 vCPU, 8 GB RAM)
  - `db.r6g.xlarge` - Memory optimized (4 vCPU, 32 GB RAM)

**allocatedStorageGb**
- What: Storage size in gigabytes
- Constraint: Must be > 0
- Range: Typically 20-65536 GB
- Example: `100`

**username**
- What: Master username for database
- Constraint: Minimum length varies by engine
- Example: `dbadmin`

**password**
- What: Master password for database
- Constraint: Minimum length varies by engine
- Note: Should be rotated with proper secrets management
- Example: `temp-password-123`

**subnetIds**
- What: VPC subnet IDs where RDS instance will be deployed
- Constraint: Need at least 2 subnets for Multi-AZ
- Format: List of subnet IDs
- Example: `["subnet-abc123", "subnet-def456"]`

**securityGroupIds**
- What: Security groups controlling network access
- Format: List of security group IDs
- Example: `["sg-xyz789"]`

### Important Optional Fields

**multiAz**
- What: Enable Multi-AZ deployment for high availability
- Type: Boolean
- Default: `false`
- Recommendation: `true` for production
- Impact: Creates standby replica in different AZ, automatic failover

**storageEncrypted**
- What: Enable encryption at rest using AWS KMS
- Type: Boolean
- Default: `false`
- Recommendation: `true` for production
- Note: Cannot be disabled after creation

**port**
- What: TCP port for database connections
- Type: Integer
- Range: 0-65535
- Defaults: 
  - Postgres: 5432
  - MySQL/MariaDB: 3306
  - Oracle: 1521
  - SQL Server: 1433

**publiclyAccessible**
- What: Assign public IP address
- Type: Boolean
- Default: `false`
- Recommendation: `false` for security (use VPN/private access)

**kmsKeyId**
- What: Custom KMS key for encryption
- Type: String (KMS key ARN)
- Note: Only used if storageEncrypted is true
- Example: `arn:aws:kms:us-east-1:123456789012:key/...`

**parameterGroupName**
- What: Custom DB parameter group
- Type: String
- Use: Override default database configuration parameters

**optionGroupName**
- What: Custom DB option group
- Type: String
- Use: Enable additional database features (Oracle/SQL Server)

**dbSubnetGroupName**
- What: Use existing DB subnet group instead of creating new one
- Type: String

## Tips & Tricks

### Getting Better Results

1. **Be Specific About Use Case**
   - Instead of: "I need a database"
   - Try: "I need a production Postgres database for a high-traffic API"
   - The agent will tailor recommendations to your use case

2. **Mention Your Resource Name Early**
   - "I want to create a database called production-api-db"
   - The agent will use your name instead of auto-generating one

3. **Ask for Recommendations**
   - "What instance size do you recommend for 10,000 requests per minute?"
   - The agent has AWS knowledge and can guide you

4. **Provide Context**
   - Mention if it's for dev, staging, or production
   - Mention expected traffic levels
   - Mention budget constraints
   - The agent will adjust recommendations accordingly

### Changing Your Mind

If you want to change a previous answer:

```
You: Actually, I want to change the instance size to db.m6g.xlarge

Agent: [Updates the requirement and confirms]
```

The agent can update individual fields without restarting the entire conversation.

### Skipping Optional Fields

If the agent asks about optional fields you don't need:

```
You: I don't need any of those optional features, let's keep it simple

Agent: [Proceeds with just required fields]
```

### Reviewing Your Choices

At any point, you can ask:

```
You: What have we configured so far?

Agent: [Uses get_collected_requirements() and shows summary]
```

## Troubleshooting

### Issue: Agent asks for subnet IDs but I don't have them

**Solution**: For proof-of-concept testing, you can use placeholder values:
```
subnet-placeholder-1, subnet-placeholder-2
```

The manifest will generate correctly, you'll just need to update these before deploying.

### Issue: Agent says my instance class is invalid

**Cause**: Instance class must start with "db."

**Solution**: 
- Instead of: `t3.micro`
- Use: `db.t3.micro`

### Issue: Agent asks too many questions

**Solution**: You can provide multiple answers at once:
```
You: Use Postgres 15.5, db.m6g.large, 100 GB storage, username dbadmin
```

The agent will extract multiple requirements from a single message.

### Issue: I made a mistake and want to start over

**Solution**: Start a new conversation in LangGraph Studio. Each conversation is independent.

### Issue: Generated manifest has placeholder org/env values

**Expected**: Currently the agent uses hardcoded defaults:
- `org: project-planton`
- `env: aws`

These will be provided by the platform context in production. For testing, you can manually edit the generated YAML.

### Issue: Password is showing in plain text

**Expected**: The manifest shows passwords in plain text because it's a YAML file.

**Best Practice**: 
1. Generate the manifest with a temporary password
2. Store the manifest in version control
3. Use your deployment system to inject the real password from a secret manager
4. Or manually replace `password: temp` with a reference to a secret

### Issue: Agent is too verbose/not verbose enough

**Solution**: Give feedback:
```
You: Can you be more concise with your questions?
```
or
```
You: Can you explain more about Multi-AZ deployment?
```

The agent will adjust its communication style.

## Advanced Usage

### Custom Labels

You can specify labels for your resource:

```
You: I want to create a database with labels team=backend and env=production
```

The agent will include these in the metadata section.

### Validating Before Generation

You can ask the agent to validate before generating:

```
You: Can you check if we have everything needed?

Agent: [Uses validate_manifest() and reports any missing/invalid fields]
```

### Regenerating with Changes

After seeing a manifest, you can request changes:

```
You: Can you regenerate this with db.m6g.xlarge instead?

Agent: [Updates the requirement and generates new manifest]
```

---

## Getting More Help

- **Quick Start**: See [QUICKSTART.md](QUICKSTART.md) for fastest path to first manifest
- **Demos**: Check [DEMO_SCENARIOS.md](DEMO_SCENARIOS.md) for more conversation examples
- **Developers**: Read [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) to understand how it works
- **Integration**: See [INTEGRATION.md](INTEGRATION.md) for production deployment guidance

