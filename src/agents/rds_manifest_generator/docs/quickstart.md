# Quick Start Guide - AWS RDS Manifest Generator

Get your first AWS RDS manifest in 5 minutes!

## Prerequisites

- Python 3.11+ installed
- Poetry installed (`brew install poetry` on macOS)
- Anthropic API key

## Step 1: Clone and Setup (2 minutes)

```bash
# Navigate to the project
cd /Users/suresh/scm/github.com/plantoncloud/graph-fleet

# Install dependencies
make venvs

# Set your API key
export ANTHROPIC_API_KEY="your-key-here"
```

## Step 2: Start the Agent (30 seconds)

```bash
make run
```

This starts LangGraph Studio. Open your browser to http://localhost:8123

## Step 3: Create Your First Manifest (2 minutes)

1. In LangGraph Studio, select the `rds_manifest_generator` graph
2. In the input box, type:

```
I want to create a Postgres database for my production API
```

3. The agent will:
   - Create a plan showing what information it needs
   - Ask you intelligent questions about your database
   - Validate your responses conversationally
   - Generate a complete YAML manifest

4. Answer the agent's questions. Here's an example conversation:

```
You: I want to create a Postgres database for my production API

Agent: Great! Let me help you create an AWS RDS Instance manifest...
       [Creates todo plan]
       What Postgres version would you like? I'd recommend 14.10 or 15.5 for production.

You: Let's use 15.5

Agent: Perfect! What instance size do you need?
       - db.t3.micro for dev/test
       - db.m6g.large for production APIs (recommended)
       - db.m6g.xlarge for high-traffic workloads

You: db.m6g.large

Agent: Great choice! How much storage in GB? For most APIs, 50-100 GB is a good start.

You: 100 GB

[Conversation continues for networking, credentials, etc...]

Agent: All set! Here's your manifest:

[Shows complete YAML manifest]
```

## What Just Happened?

The agent did several intelligent things:

1. **Understood Context** - It knew you wanted a production database and asked appropriate questions
2. **Used Schema Knowledge** - It queried the AWS RDS protobuf schema to understand requirements and validation rules
3. **Provided Guidance** - It suggested sensible defaults based on your use case
4. **Validated Conversationally** - It checked your responses against validation rules (e.g., instance_class must start with "db.")
5. **Generated the Manifest** - It converted all collected requirements into a properly formatted YAML manifest

## The Magic Behind It

This agent uses:

- **LangGraph + DeepAgents** - For robust conversational AI with tool use
- **Proto Schema Understanding** - Dynamically parses AWS RDS protobuf definitions
- **AI-Driven Questions** - No hardcoded templates; questions are generated from schema + AWS knowledge
- **Soft Validation** - Validates responses using proto rules, but explains errors conversationally

## Your Manifest

The generated manifest looks like this:

```yaml
apiVersion: aws.project-planton.org/v1
kind: AwsRdsInstance
metadata:
  name: postgres-instance-abc123
  org: project-planton
  env: aws
spec:
  engine: postgres
  engineVersion: "15.5"
  instanceClass: db.m6g.large
  allocatedStorageGb: 100
  username: dbadmin
  password: your-secure-password
  # ... other fields you configured
```

You can save this to a file and deploy it with Planton Cloud:

```bash
planton apply -f rds-instance.yaml
```

## Next Steps

- **Try Different Scenarios** - Create MySQL, MariaDB, or Oracle databases
- **Explore Features** - Ask for Multi-AZ, encryption, custom ports
- **Read the User Guide** - See [USER_GUIDE.md](user_guide.md) for detailed examples
- **Understand the Code** - Check [DEVELOPER_GUIDE.md](developer_guide.md) to learn how it works

## Troubleshooting

**Agent doesn't start?**
- Make sure you've run `make venvs` to install dependencies
- Check that your ANTHROPIC_API_KEY is set

**Agent asks for strange values?**
- The agent is reading from the actual AWS RDS protobuf schema
- Some fields like subnet_ids and security_group_ids are AWS-specific
- You can provide placeholder values for testing

**Want to start over?**
- Just start a new conversation in LangGraph Studio
- Each conversation is independent

## Getting Help

- Check [USER_GUIDE.md](user_guide.md) for common questions
- Review [DEMO_SCENARIOS.md](demo_scenarios.md) for example conversations
- See [DEVELOPER_GUIDE.md](developer_guide.md) for technical details

---

**Time to First Manifest**: ~5 minutes  
**Complexity**: Just answer questions naturally  
**Output**: Production-ready YAML manifest

