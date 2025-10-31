# Security Policy

## Reporting a Vulnerability

We take the security of graph-fleet seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### Where to Report

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to:

- **Email**: support@planton.ai
- **Subject**: [SECURITY] graph-fleet - Brief description

### What to Include

When reporting a vulnerability, please include the following information:

1. **Type of vulnerability** (e.g., SQL injection, XSS, credential exposure)
2. **Full paths of source file(s)** related to the vulnerability
3. **Location** of the affected source code (tag/branch/commit or direct URL)
4. **Step-by-step instructions** to reproduce the issue
5. **Proof-of-concept or exploit code** (if possible)
6. **Impact** of the vulnerability (what an attacker could achieve)
7. **Any special configuration required** to reproduce the issue

### What to Expect

After you submit a report, we will:

1. **Acknowledge receipt** of your vulnerability report within 48 hours
2. **Provide an initial assessment** within 5 business days
3. **Keep you informed** of our progress towards a fix
4. **Notify you** when the vulnerability has been fixed
5. **Credit you** in our security advisory (unless you prefer to remain anonymous)

### Our Commitment

- We will work with you to understand and resolve the issue quickly
- We will keep you informed throughout the process
- We will not take legal action against researchers who:
  - Report vulnerabilities in good faith
  - Make a good faith effort to avoid privacy violations and data destruction
  - Do not exploit the vulnerability beyond what is necessary to demonstrate it

## Supported Versions

We release patches for security vulnerabilities on the following versions:

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |
| < 1.0   | :x:                |

## Security Features

This repository has the following security features enabled:

- ✅ **Secret Scanning**: Automatically detects accidentally committed secrets
- ✅ **Push Protection**: Blocks pushes that contain detected secrets
- ✅ **Dependabot Alerts**: Notifies of vulnerable dependencies
- ✅ **Dependabot Security Updates**: Automatically creates PRs to update vulnerable dependencies
- ✅ **Branch Protection**: Main branch is protected with required reviews
- ✅ **Code Owners**: Designated owners review sensitive changes

## Security Best Practices for Contributors

When contributing to this project, please:

1. **Never commit secrets** (API keys, passwords, tokens, certificates)
   - Use environment variables instead
   - Add sensitive file patterns to `.gitignore`
   
2. **Keep dependencies up to date**
   - Review and merge Dependabot PRs promptly
   - Check for security advisories regularly

3. **Follow secure coding practices**
   - Validate all inputs
   - Use parameterized queries
   - Sanitize user-provided data
   - Implement proper authentication and authorization

4. **Review code carefully**
   - Pay special attention to security-sensitive areas
   - Question unusual patterns or overly complex code
   - Verify that secrets management is done correctly

5. **Use the security tools**
   - Set up pre-commit hooks (see `.pre-commit-config.yaml`)
   - Run security scans locally before pushing
   - Address any security warnings from linters

## Recent Security Incidents

### November 1, 2025: Credential Exposure
- **Issue**: `.env_export` file containing API keys was accidentally committed
- **Resolution**: File removed from git history, secret scanning enabled
- **Lesson**: Always use `.gitignore` and enable push protection
- **Status**: Resolved - see `SENSITIVE_DATA_REMOVAL_SUMMARY.md` for details

## Additional Resources

- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)

## Contact

For any questions about security policies or practices:
- Email: security@planton.cloud
- Repository: https://github.com/plantoncloud-inc/graph-fleet

---

**Last Updated**: November 1, 2025

