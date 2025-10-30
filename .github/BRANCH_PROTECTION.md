# GitHub Branch Protection for Graph Fleet

This document explains how branch protection is configured for the Graph Fleet repository to ensure code quality and prevent broken code from being merged.

## Overview

Branch protection rules are enabled on the `main` branch to enforce that all pull requests must pass the **"Validate Python Code"** workflow before they can be merged. This ensures that:

- ✅ All code passes Ruff linting checks
- ✅ All code passes MyPy type checking
- ✅ Import errors are caught before merging
- ✅ Code quality standards are maintained

## Current Protection Rules

The `main` branch has the following protection rules enabled:

### Required Status Checks
- **Status Check Name**: `Lint and Type Check`
- **Source**: `.github/workflows/validate.yml`
- **Requirement**: Must pass before merging
- **Up-to-date requirement**: Branches must be up to date with `main` before merging

### Workflow Details
The workflow runs on every pull request and performs:
1. Ruff linting (`poetry run ruff check .`)
2. MyPy type checking (`poetry run mypy --config-file mypy.ini src/`)

## Setting Up Branch Protection

Branch protection rules are **repository settings**, not code-based configuration. They must be set up by someone with admin access to the repository.

### Option 1: Automated Setup (Recommended)

Use the provided script to apply branch protection rules automatically:

```bash
# Navigate to the repository root
cd /path/to/graph-fleet

# Run the setup script
./.github/scripts/setup-branch-protection.sh
```

**Requirements:**
- GitHub CLI (`gh`) installed and authenticated
- Admin permissions on the `plantoncloud-inc/graph-fleet` repository

**Installation of GitHub CLI:**
```bash
# macOS
brew install gh

# Linux
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# Authenticate
gh auth login
```

### Option 2: Manual Setup via GitHub UI

If you prefer to configure branch protection manually or don't have the GitHub CLI:

1. **Navigate to Branch Protection Settings:**
   - Go to: https://github.com/plantoncloud-inc/graph-fleet/settings/branches
   - (Requires admin access)

2. **Add or Edit Branch Protection Rule:**
   - Click "Add rule" (or "Edit" if a rule already exists for `main`)
   - **Branch name pattern**: `main`

3. **Configure Required Settings:**
   - ✅ Check **"Require status checks to pass before merging"**
   - ✅ Check **"Require branches to be up to date before merging"**
   - In the status checks search box, type and select: **`Lint and Type Check`**
     - ⚠️ Note: This status check will only appear in the list after the workflow has run at least once
   
4. **Optional Settings** (recommended):
   - ✅ Check **"Require a pull request before merging"**
     - This prevents direct pushes to `main`
   - ✅ Check **"Require conversation resolution before merging"**
     - Ensures all review comments are addressed

5. **Save Changes:**
   - Click "Create" or "Save changes"

## Verifying Branch Protection

After setting up branch protection, verify it's working:

### Test 1: Create a Test PR with Failing Code

```bash
# Create a new branch
git checkout -b test-branch-protection

# Add a file with a linting error (undefined variable)
echo "print(undefined_variable)" > test_file.py

# Commit and push
git add test_file.py
git commit -m "Test branch protection"
git push origin test-branch-protection

# Create a PR via GitHub UI or CLI
gh pr create --title "Test Branch Protection" --body "Testing workflow enforcement"
```

**Expected Result:**
- The workflow runs automatically
- The "Lint and Type Check" status check fails
- The merge button is disabled or shows a warning
- You cannot merge the PR until the workflow passes

### Test 2: Fix the Code and Verify Merge

```bash
# Fix the code
echo "print('Hello, World!')" > test_file.py

# Commit and push the fix
git add test_file.py
git commit -m "Fix linting error"
git push origin test-branch-protection
```

**Expected Result:**
- The workflow runs again
- The "Lint and Type Check" status check passes
- The merge button becomes enabled
- You can now merge the PR

## Troubleshooting

### Issue: Status check "Lint and Type Check" doesn't appear in the settings

**Cause:** The workflow hasn't run yet, so GitHub doesn't know about this status check.

**Solution:**
1. Create a test PR to trigger the workflow
2. Wait for the workflow to complete
3. Return to branch protection settings
4. The status check should now appear in the search results

### Issue: PRs can still be merged even though the workflow failed

**Cause:** Branch protection rules are not configured correctly.

**Solution:**
1. Verify you're looking at the correct branch (`main`)
2. Check that "Require status checks to pass before merging" is enabled
3. Verify "Lint and Type Check" is listed under required status checks
4. Ensure the status check name matches exactly (case-sensitive)

### Issue: "Lint and Type Check" workflow passes but merge is still blocked

**Cause:** Branch is not up to date with `main`.

**Solution:**
1. Merge or rebase your branch with the latest `main`
2. Push the updated branch
3. Wait for the workflow to run again on the updated code

### Issue: Script fails with "permission denied"

**Cause 1:** You don't have admin permissions on the repository.

**Solution:** Ask a repository admin to run the script or manually configure the settings.

**Cause 2:** The script is not executable.

**Solution:**
```bash
chmod +x .github/scripts/setup-branch-protection.sh
```

### Issue: GitHub CLI authentication fails

**Solution:**
```bash
# Re-authenticate
gh auth logout
gh auth login

# Follow the prompts to authenticate
```

## Workflow File Reference

The validation workflow is defined in `.github/workflows/validate.yml`:

```yaml
name: Validate Python Code

on:
  pull_request:
    branches: [main]

jobs:
  validate:
    name: Lint and Type Check
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install Poetry
        run: |
          pipx install poetry
          poetry --version
      
      - name: Install dependencies
        run: poetry install --no-interaction --no-ansi
      
      - name: Run Ruff linter
        run: poetry run ruff check . --output-format=github
      
      - name: Run MyPy type checker
        run: poetry run mypy --config-file mypy.ini src/
```

**Important:** The job name `Lint and Type Check` must match exactly in the branch protection settings. If you rename this job, you must update the branch protection rules accordingly.

## Bypassing Branch Protection (Admins Only)

Repository admins can bypass branch protection rules. However, this is **strongly discouraged** as it defeats the purpose of having these checks.

If you absolutely must merge code that fails validation:
1. Understand why the checks are failing
2. Fix the issues if possible
3. If the checks themselves are broken, fix the workflow first
4. Only bypass as a last resort for urgent hotfixes

To prevent even admins from bypassing:
- Edit the script and set `enforce_admins=true`
- Or enable "Do not allow bypassing the above settings" in the GitHub UI

## Updating Branch Protection

If you need to modify the branch protection rules:

1. **Edit the script**: Update `.github/scripts/setup-branch-protection.sh`
2. **Run the script**: `./github/scripts/setup-branch-protection.sh`
3. **Or use GitHub UI**: Manually update at https://github.com/plantoncloud-inc/graph-fleet/settings/branches

## Additional Resources

- [GitHub Branch Protection Documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub Actions Status Checks](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories-with-code-quality-features/about-status-checks)
- [GitHub CLI Documentation](https://cli.github.com/manual/)
- [Graph Fleet README](../README.md) - Local development and validation

## Support

If you encounter issues not covered in this documentation:
1. Check the [GitHub Actions runs](https://github.com/plantoncloud-inc/graph-fleet/actions) for error details
2. Review the [workflow file](.github/workflows/validate.yml) for configuration
3. Contact a repository administrator for permission-related issues

