# Demos Directory

This directory contains demonstration scripts that show how credential handling works in the AWS ECS Deep Agent.

## Files

### `simple_credential_demo.py`
Interactive demonstration showing:
- How credentials flow between subagents  
- Isolation between different agent invocations
- Why global context is problematic

Run with: `python3 simple_credential_demo.py`

### `demo_credential_isolation.py` 
Detailed demonstration of credential isolation with:
- Concurrent agent sessions
- Sequential agent sessions
- Global context problems

Run with: `python3 demo_credential_isolation.py`

### `standalone_credential_test.py`
Simplified test showing the complete credential flow without external dependencies.
Great for understanding the architecture.

Run with: `python3 standalone_credential_test.py`

## Key Concepts Demonstrated

1. **Credential Sharing**: How subagents within one invocation share credentials
2. **Session Isolation**: How different invocations must have isolated credentials
3. **Security Issues**: Why the current global singleton approach is unsafe
4. **Proper Architecture**: How session-based contexts solve the problem

## Important Note

These demos show both:
- ✅ How it SHOULD work (with session isolation)
- ❌ How it currently works (with global singleton - UNSAFE)

The actual implementation in `../agent.py` needs to be updated to match the proper architecture shown in these demos.
