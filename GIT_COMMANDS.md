# 📝 Git Commit & Deployment Commands

## Step-by-Step Git Commands

### 1. Check Current Status
```bash
cd /home/ibrahim/ibrahimmutisiaportfolio
git status
```

Expected output: Shows modified and new files

### 2. Add All Changes
```bash
git add -A
```

This adds:
- New Procfile
- Modified settings.py
- Modified build.sh
- Modified contact.html
- All documentation files

### 3. Verify Changes Are Staged
```bash
git status
```

Expected output: All files show as "Changes to be committed"

### 4. Commit with Descriptive Message
```bash
git commit -m "Fix: Add Procfile for Render, optimize deployment, fix settings and templates

- Add critical Procfile for proper Render deployment flow
- Fix settings.py: add SECRET_KEY fallback, email defaults, HTTPS proxy header
- Optimize build.sh: error handling, remove duplicates, add logging
- Fix contact.html: close HTML tags, improve structure
- Add comprehensive deployment documentation"
```

Or use simpler message:
```bash
git commit -m "Fix deployment issues: Add Procfile, fix settings, optimize build process"
```

### 5. Push to GitHub
```bash
git push origin main
```

Expected output: 
```
To github.com:ibrahim-640/ibrahimmutisiaportfolio.git
   [commit-hash] master -> master
```

### 6. Verify Push Successful
```bash
git log -1 --oneline
```

Should show your commit at the top.

---

## Complete One-Liner (If You Know What You're Doing)

```bash
cd /home/ibrahim/ibrahimmutisiaportfolio && git add -A && git commit -m "Fix: Add Procfile, optimize deployment, fix settings.py and templates" && git push origin main
```

---

## After Git Push: Render Deployment

### In Render Dashboard:

1. **Go to:** https://render.com/dashboard
2. **Find your service:** Look for "personal-website-w377" or similar
3. **Click on it**
4. **Scroll to bottom**
5. **Click "Clear build cache & redeploy"**
6. **Wait 2-3 minutes**
7. **Check Logs tab** for success

---

## Verification After Push

Check that GitHub has your changes:
```bash
git remote -v
# Should show: origin pointing to your repo

git branch -a
# Should show: main branch

git log --oneline -5
# Should show your recent commits
```

---

## If Something Goes Wrong with Git

### Undo Last Commit (Before Push)
```bash
git reset --soft HEAD~1
# Then modify files and commit again
```

### Undo Last Commit (After Push)
```bash
git revert HEAD
git push origin main
```

### Check What Changed
```bash
git diff HEAD
# Shows all uncommitted changes

git diff HEAD~1
# Shows changes from last commit
```

### See Commit History
```bash
git log --oneline -10
# Shows last 10 commits
```

---

## Files Being Committed

### New Files:
```
Procfile
DEPLOYMENT_ANALYSIS.md
RENDER_DEPLOYMENT_GUIDE.md
ENV_VARIABLES_SETUP.md
PROBLEM_SUMMARY.md
QUICK_REFERENCE.md
BEFORE_AND_AFTER.md
FINAL_DEPLOYMENT_CHECKLIST.md
GIT_COMMANDS.md (this file)
```

### Modified Files:
```
portfolio_site/settings.py
portfolio_site/build.sh
portfolio_site/templates/contact.html
```

### Not Committed (Ignored):
```
.env (should be in .gitignore)
db.sqlite3 (local database)
__pycache__/ (Python cache)
staticfiles/ (generated on Render)
```

---

## Commit Message Explanation

**Good commit message includes:**
- ✅ What was fixed (Fix: ...)
- ✅ Why it was fixed (context)
- ✅ List of changes (bullet points)

**Example:**
```
Fix: Add Procfile for Render deployment

- Add Procfile with release and web phases
- Fix settings.py SECRET_KEY handling
- Optimize build.sh
- Fix template HTML structure
```

---

## Next Steps After Push

1. ✅ Code pushed to GitHub
2. ⏳ Wait for Render to detect change
3. ⏳ Render automatically rebuilds (or manually trigger)
4. ⏳ Build completes (2-3 minutes)
5. ⏳ Site goes live
6. ✅ Verify at https://personal-website-w377.onrender.com

---

## Quick Status Check

At any time, run:
```bash
cd /home/ibrahim/ibrahimmutisiaportfolio
git status
git log --oneline -3
```

This shows:
- Any uncommitted changes
- Recent commits
- Current branch

---

## GitHub Integration with Render

Render automatically:
1. ✅ Watches your GitHub repo
2. ✅ Detects new pushes to main branch
3. ✅ Triggers automatic rebuild
4. ✅ Deploys updated code

You can also manually trigger:
- Render Dashboard → Your Service → "Clear build cache & redeploy"

---

## Troubleshooting Git

### "fatal: not a git repository"
```bash
cd /home/ibrahim/ibrahimmutisiaportfolio
# Make sure you're in correct directory
```

### "nothing to commit, working tree clean"
```bash
git status
# All changes already committed
# Either push to GitHub, or make new changes
```

### "Updates were rejected"
```bash
# Your GitHub repo is ahead of local
git pull origin main
# Then make your changes and push
```

### "Permission denied (publickey)"
```bash
# SSH key issue
# Either use HTTPS: git remote set-url origin https://...
# Or add SSH key to GitHub
```

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `git status` | Check current status |
| `git add -A` | Stage all changes |
| `git commit -m "msg"` | Create commit |
| `git push origin main` | Push to GitHub |
| `git log --oneline` | View commit history |
| `git diff` | See changes |
| `git reset --soft HEAD~1` | Undo last commit |

---

## Final Checklist Before Push

- [ ] All files modified correctly
- [ ] Django check passes
- [ ] Procfile exists in portfolio_site/
- [ ] Build.sh is executable
- [ ] Contact.html has no HTML errors
- [ ] Settings.py has SECRET_KEY fallback
- [ ] No .env file in git (should be in .gitignore)
- [ ] Commit message is descriptive

Then:
```bash
git push origin main
```

And then redeploy in Render Dashboard.

**You're all set! 🚀**

