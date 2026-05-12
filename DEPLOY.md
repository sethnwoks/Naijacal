# 🚀 DEPLOYMENT GUIDE - NAIJACAL

## Quick Deploy to Render + Vercel (FREE)

### Step 1: Push to GitHub (DO THIS FIRST)

```bash
cd /home/sethoski/Health_App

# Make sure you're in the right directory
git status

# Add all files
git add .

# Commit
git commit -m "Initial commit: NaijaCal - Nigerian food calorie tracker"

# Create repo on GitHub (do this on github.com)
# Then add remote and push:
git remote add origin https://github.com/YOUR_USERNAME/naijacal.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy Backend to Render

1. Go to https://render.com and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repo
4. Configure:
   - **Name:** naijacal-backend
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt && python manage.py migrate`
   - **Start Command:** `gunicorn core.wsgi:application`
   - **Add Environment Variables:**
     - `GEMINI_API_KEY` = your Gemini key
     - `DEBUG` = False
     - `PYTHON_VERSION` = 3.12.0
5. Click "Create Web Service"
6. Copy your Render URL (e.g., `https://naijacal-backend.onrender.com`)

### Step 3: Deploy Frontend to Vercel

1. Go to https://vercel.com and sign up
2. Click "Add New" → "Project"
3. Import your GitHub repo
4. Configure:
   - **Framework Preset:** Create React App
   - **Root Directory:** `frontend/frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `build`
   - **Add Environment Variable:**
     - `REACT_APP_API_URL` = Your Render URL from Step 2
5. Click "Deploy"
6. Copy your Vercel URL

### Step 4: Update Your Backend CORS

On Render dashboard:
1. Go to your backend service
2. Click "Environment"
3. Add/Update:
   - `CORS_ALLOWED_ORIGINS` = Your Vercel URL
4. Save and redeploy

### Step 5: Update Your README

Replace in README.md:
- `[Add your Render URL here]` → Your actual Render URL
- `[@yourusername]` → Your actual GitHub username
- Add screenshots (take them from the live app)

### Step 6: Test It Live

1. Visit your Vercel URL
2. Try parsing: "Breakfast: Jollof rice and chicken"
3. If it works → YOU'RE LIVE! 🎉
4. If it doesn't → Check Render logs

## Common Issues

### Backend won't start on Render
- Check environment variables are set
- Check Python version is 3.12
- Look at Render logs for errors

### Frontend can't connect to backend
- Check CORS_ALLOWED_ORIGINS includes your Vercel URL
- Check REACT_APP_API_URL is correct
- Open browser console for errors

### Database issues
- Render provides free PostgreSQL
- Add it from Render dashboard → Internal Database
- Copy DATABASE_URL to your environment variables

## After Deployment

Update your CV/LinkedIn with:
- **Live Demo:** [Your Vercel URL]
- **Source Code:** [Your GitHub URL]
- **Stack:** Django, React, PostgreSQL, Google Gemini AI

---

Total time to deploy: **30-45 minutes**
Total cost: **$0** (both platforms have free tiers)

🔥 Now go get that job!
