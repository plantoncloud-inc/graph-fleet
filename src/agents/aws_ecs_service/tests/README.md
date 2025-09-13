# Tests Directory

This directory contains test files for the AWS ECS Deep Agent.

## Test Files

### `verify_isolation.py`
Core test that verifies credential isolation works correctly:
- Tests basic context isolation
- Tests concurrent operations  
- Tests cleanup mechanism
- Simulates graph invocations
- Shows credential sharing within invocations
- Demonstrates isolation between invocations
- No external dependencies required

### `TEST_RESULTS.md`
Summary of test results and findings from running the test.

## Running Tests

```bash
cd tests/
python3 verify_isolation.py
```

The test runs without external dependencies and comprehensively verifies that the credential isolation implementation is working correctly.
