# COMPLETE GUIDE TO PUSH YOUR PORTFOLIO TO RENDER

## STEP-BY-STEP INSTRUCTIONS

### STEP 1: Verify Your Changes Locally (Copy & Paste These Commands)

```bash
# Open terminal and navigate to your project
cd /home/ibrahim/ibrahimmutisiaportfolio

# Check that critical files exist
ls -la Procfile
ls -la build.sh  
ls -la .gitignore
ls -la portfolio_site/portfolio_site/settings.py

# Verify settings.py has the email config fix
grep -A 5 "try:" portfolio_site/portfolio_site/settings.py | grep -A 5 "EMAIL_HOST_USER"

# Test collectstatic locally
cd portfolio_site
python3 manage.py collectstatic --noinput --clear
ls -la staticfiles/css/style.css
cd ..
```

**Expected Results:**
- ✅ All 4 files should exist and list with timestamps
- ✅ Settings.py should show try/except block around EMAIL_HOST_USER
- ✅ staticfiles/css/style.css should be created

---

### STEP 2: Initialize Git & Commit Changes

```bash
cd /home/ibrahim/ibrahimmutisiaportfolio

# Initialize git repo
git init
git config user.name "Ibrahim Mutisia"
git config user.email "mwitaibrahim88@gmail.com"

# Add all files
git add -A

# Verify files are staged
git status

# Commit
git commit -m "Fix: Static files and email config for Render deployment"

# Verify commit was created
git log --oneline -1
```

**Expected Output:**
```
On branch master

Initial commit
create mode 100644 .gitignore
create mode 100644 Procfile
create mode 100755 build.sh
...
portfolio_site/ folder with all contents
```

---

### STEP 3: Add Render Remote & Push

**IMPORTANT:** You need your Render repository URL. Find it here:

1. Go to https://dashboard.render.com/
2. Click on your service (portfolio or whatever name)
3. Click **Settings** tab on the left
4. Look for **Repository** section
5. Copy the HTTPS URL (should look like: `https://github.com/YOUR-USERNAME/YOUR-REPO.git`)

Then run:

```bash
cd /home/ibrahim/ibrahimmutisiaportfolio

# Add Render as remote (replace URL below with your actual repo URL)
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git

# Verify remote is set
git remote -v

# Push to main branch
git push -u origin main

# OR if your branch is different:
# git push -u origin master
```

**Expected Output:**
```
...
To https://github.com/YOUR-USERNAME/YOUR-REPO.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

---

### STEP 4: Configure Environment Variables on Render

1. Go to https://dashboard.render.com/
2. Click your service
3. Go to **Environment** tab
4. Add these variables (if not already set):

| Variable | Value | Notes |
|----------|-------|-------|
| `DEBUG` | `False` | MUST be False in production |
| `SECRET_KEY` | Generate at https://djecrety.ir/ | Copy entire string |
| `PYTHONUNBUFFERED` | `1` | For logging |

**How to add a variable:**
- Click "Add Environment Variable"
- Enter key name (e.g., "DEBUG")
- Enter value (e.g., "False")
- Click checkmark to save

---

### STEP 5: Clear Cache & Redeploy

1. Go to https://dashboard.render.com/
2. Click your service
3. Scroll down to **Manual Deploy** section
4. Check the box: ☑️ **Clear build cache**
5. Click **Deploy latest commit**
6. Watch the build logs

**What to look for in logs:**
```
✅ "Installing dependencies..."
✅ "pip install -r requirements.txt"
✅ "Collecting static files..."
✅ "130 static files copied to '/opt/render/project/src/portfolio_site/staticfiles'"
✅ "Build complete"
✅ Started server...
```

---

### STEP 6: Verify Static Files Load

Once deployment finishes (takes 2-3 minutes):

```bash
# Test CSS file loads
curl -I https://YOUR-APP-NAME.onrender.com/static/css/style.css

# Replace YOUR-APP-NAME with your actual Render service name
# Example: https://ibrahim-portfolio.onrender.com/static/css/style.css
```

**Expected Output:**
```
HTTP/2 200
content-type: text/css
cache-control: max-age=60, public
...
```

If you get 404, see troubleshooting below.

---

### STEP 7: Open Your Live Site

1. Visit: `https://YOUR-APP-NAME.onrender.com/`
2. Open DevTools (F12 or Cmd+Option+I)
3. Go to **Network** tab
4. Reload the page
5. Check that CSS files load with **200** status (not 404)
6. Styles should be visible!

---

## TROUBLESHOOTING

### Problem: Still Getting 404 on Static Files

**Check 1: Verify collectstatic ran**
- In Render build logs, search for "130 static files copied"
- If not present, the release step didn't execute

**Fix:**
```bash
cd /home/ibrahim/ibrahimmutisiaportfolio
# Verify Procfile is at repo root (not in subfolder)
cat Procfile

# Should show:
# release: cd portfolio_site && python3 manage.py collectstatic --noinput && python3 manage.py migrate
# web: cd portfolio_site && gunicorn portfolio_site.wsgi:application --log-file -
```

### Problem: Deployment Fails with Error

**Check the error message in logs:**

If error mentions `EMAIL_HOST_USER`:
- Verify settings.py has try/except block (lines ~150-165)
- Confirm it looks like:
```python
try:
    EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
    EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
except Exception:
    EMAIL_HOST_USER = ""
    EMAIL_HOST_PASSWORD = ""
```

If error mentions `Procfile`:
- Make sure `Procfile` is in repo root, not in `portfolio_site/`
- Check it's executable: `chmod +x Procfile` (on Linux)

### Problem: CSS Loads but Styles Don't Apply

**Possible causes:**
1. MIME type blocking - Check browser console for CSP warnings
2. File encoding issue - Unlikely if using CompressedManifestStaticFilesStorage

**Fix:**
- Open DevTools → Console
- Look for warnings about Content-Security-Policy or MIME type
- If CSP warning: may need to update security headers (contact me)

---

## SUMMARY OF WHAT WAS FIXED

| Issue | Solution | File |
|-------|----------|------|
| Email config crashes Django on startup | Added try/except fallback | `portfolio_site/settings.py` |
| collectstatic doesn't run on Render | Created root-level Procfile | `Procfile` (new) |
| Static files not collected in subfolder | Created root-level build.sh | `build.sh` (new) |
| Unnecessary files in git | Created .gitignore | `.gitignore` (new) |

---

## QUICK REFERENCE: All Commands in Order

```bash
# 1. Verify everything works locally
cd /home/ibrahim/ibrahimmutisiaportfolio
python3 manage.py collectstatic --noinput --clear

# 2. Initialize git
git init
git config user.name "Ibrahim Mutisia"
git config user.email "mwitaibrahim88@gmail.com"
git add -A
git commit -m "Fix: Static files and email config for Render"

# 3. Add remote (get URL from Render dashboard first!)
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
git push -u origin main

# 4. Set env vars on Render dashboard (DEBUG=False, SECRET_KEY, PYTHONUNBUFFERED=1)

# 5. Manual deploy with cache clear on Render

# 6. Test
curl -I https://YOUR-APP.onrender.com/static/css/style.css
```

---

## Need Help?

If any step fails:
1. Copy the **exact error message** from the logs
2. Note which **STEP** failed
3. Provide any **terminal output**

I'll help you fix it immediately!

