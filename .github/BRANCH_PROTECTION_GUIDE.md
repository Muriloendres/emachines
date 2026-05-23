# Branch Protection Rules Setup Guide

This guide explains how to set up branch protection rules for the `main` branch to ensure code quality and prevent accidental changes.

## Why Branch Protection?

Branch protection rules enforce:
- ✓ Code reviews before merge
- ✓ Tests pass before merge
- ✓ No direct pushes to main (requires PR)
- ✓ Clear ownership and responsibility

## Setup Instructions

### Step 1: Go to Repository Settings
1. Go to your GitHub repository
2. Click **Settings** (top right)
3. Click **Branches** (left sidebar)

### Step 2: Add a Branch Protection Rule
1. Click **Add rule** button
2. Under "Branch name pattern", enter: `main`
3. Click **Create**

### Step 3: Configure Protection Settings

#### ✅ **Require a pull request before merging**
- Check: "Require a pull request before merging"
- Check: "Require approval from pull request reviews"
- Set required approvals: **1**
- Check: "Dismiss stale pull request approvals when new commits are pushed"
- Check: "Require review from Code Owners" (if using CODEOWNERS file)

**Why:** Every change must be reviewed by the maintainer before merging.

#### ✅ **Require status checks to pass before merging**
- Check: "Require status checks to pass before merging"
- Check: "Require branches to be up to date before merging"

**Why:** Tests must pass and code must be updated with the latest main branch.

#### ✅ **Require conversation resolution before merging**
- Check: "Require conversation resolution before merging"

**Why:** All review comments must be addressed before merge.

#### ✅ **Include administrators**
- Check: "Include administrators" (optional but recommended)

**Why:** Ensures rules apply to everyone, including owners.

#### ✅ **Restrict who can push to matching branches**
- Uncheck this (leave it off) to allow contributors to push to feature branches

**Why:** Contributors should be able to push to their own branches.

#### ✅ **Allow force pushes**
- Uncheck: "Allow force pushes" (leave it off)

**Why:** Prevents accidental history rewrites.

#### ✅ **Automatically delete head branches**
- Check: "Automatically delete head branches"

**Why:** Keeps the repository clean by removing merged branch copies.

### Step 4: Save Configuration

Click **Save changes** at the bottom.

## Result

Your main branch is now protected! Here's what happens:

| Action | Before | After |
|--------|--------|-------|
| Direct push to main | ❌ Allowed | ✅ **Blocked** |
| PR without review | ❌ Allowed | ✅ **Blocked** |
| Merge with failing tests | ❌ Allowed | ✅ **Blocked** |
| Merge without approval | ❌ Allowed | ✅ **Blocked** |

## Workflow for Contributors

With these rules in place:

```
1. Create feature branch (push is allowed)
   git checkout -b feature/my-feature

2. Make changes and commit
   git commit -m "Add new feature"

3. Push to GitHub
   git push origin feature/my-feature

4. Create Pull Request
   → Tests automatically run
   → Maintainer reviews
   → Maintainer approves

5. Merge (only maintainer can do this)
   → Automatic merge on approve + tests pass
   → Branch automatically deleted
```

## Testing Your Setup

To verify the rules work:

1. **Try pushing directly to main** (should fail):
   ```bash
   git checkout main
   git commit --allow-empty -m "Test"
   git push origin main
   # Should get: "remote: error: force-pushing to main is not allowed"
   ```

2. **Create a PR with failing tests** and verify it can't be merged
3. **Approve and merge a PR** to confirm the workflow works

## FAQ

**Q: Can I bypass these rules?**
- A: Only if you disable the rule. Don't do this without a good reason.

**Q: What if I need to push directly to main in an emergency?**
- A: Temporarily disable the rule, push, then re-enable. Always document why.

**Q: Do these rules apply to me as the owner?**
- A: Yes, if you check "Include administrators". This is a best practice.

**Q: Can multiple reviewers be required?**
- A: Yes! Set "required approvals" to 2+ if you want multiple reviews.

## Next Steps

- Share this setup with your collaborators
- Verify they understand the PR workflow
- Practice with a test PR to ensure everything works

---

**Your repository is now set up for safe, collaborative development! 🎉**
