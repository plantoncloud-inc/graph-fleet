#!/bin/bash
set -e

# GitHub Branch Protection Setup Script for Graph Fleet
# This script configures branch protection rules for the main branch
# to require the "Validate Python Code" workflow to pass before merging PRs.
#
# Requirements:
# - GitHub CLI (gh) installed and authenticated
# - Admin permissions on the repository
#
# Usage:
#   ./setup-branch-protection.sh

REPO="plantoncloud-inc/graph-fleet"
BRANCH="main"
STATUS_CHECK="Lint and Type Check"

echo "=========================================="
echo "GitHub Branch Protection Setup"
echo "=========================================="
echo "Repository: $REPO"
echo "Branch: $BRANCH"
echo "Required Status Check: $STATUS_CHECK"
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ Error: GitHub CLI (gh) is not installed."
    echo "Please install it from: https://cli.github.com/"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "❌ Error: GitHub CLI is not authenticated."
    echo "Please run: gh auth login"
    exit 1
fi

echo "✅ GitHub CLI is installed and authenticated"
echo ""

# Confirm with user
read -p "This will update branch protection rules for $BRANCH. Continue? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 0
fi

echo ""
echo "Applying branch protection rules..."
echo ""

# Apply branch protection rules using GitHub API via gh CLI
# Note: This uses the REST API to set up branch protection
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "/repos/$REPO/branches/$BRANCH/protection" \
  -f required_status_checks[strict]=true \
  -f "required_status_checks[contexts][]=$STATUS_CHECK" \
  -f required_pull_request_reviews[dismiss_stale_reviews]=false \
  -f required_pull_request_reviews[require_code_owner_reviews]=false \
  -f required_pull_request_reviews[required_approving_review_count]=0 \
  -f enforce_admins=false \
  -f required_linear_history=false \
  -f allow_force_pushes=false \
  -f allow_deletions=false \
  -f block_creations=false \
  -f required_conversation_resolution=false \
  > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Branch protection rules successfully applied!"
    echo ""
    echo "Configuration Summary:"
    echo "  • Required status check: $STATUS_CHECK"
    echo "  • Branches must be up to date before merging"
    echo "  • Pull requests can be merged without reviews (0 required)"
    echo "  • Admins can bypass these rules"
    echo ""
    echo "View settings at:"
    echo "https://github.com/$REPO/settings/branches"
else
    echo "❌ Failed to apply branch protection rules."
    echo ""
    echo "Common issues:"
    echo "  • You may not have admin permissions on the repository"
    echo "  • The branch '$BRANCH' may not exist"
    echo "  • The API endpoint may have changed"
    echo ""
    echo "Try applying the rules manually via the GitHub UI:"
    echo "https://github.com/$REPO/settings/branches"
    exit 1
fi

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "PRs targeting '$BRANCH' now require:"
echo "  1. The '$STATUS_CHECK' workflow to pass"
echo "  2. The branch to be up to date with '$BRANCH'"
echo ""
echo "Note: These rules can be bypassed by repository admins."
echo "To enforce rules for admins, update 'enforce_admins' in this script."

