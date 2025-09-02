# Free Deployment: Vercel + Railway

## 🚀 Deploy Backend to Railway (Free)

1. **Push to GitHub** (if not already):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Deploy to Railway**:
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-detect Django and deploy

3. **Set Environment Variables** in Railway dashboard:
   - `SECRET_KEY`: `your-secret-key-here`
   - `DEBUG`: `False`
   - `DATABASE_URL`: (Railway provides PostgreSQL for free)

## 🌐 Deploy Frontend to Vercel (Free)

1. **Deploy to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Sign up with GitHub
   - Click "New Project"
   - Select your repository
   - Set **Root Directory**: `echopredict_frontend`
   - Deploy

2. **Update API URLs** in your React app to use Railway backend URL

## 📝 After Deployment

- **Backend URL**: `https://your-app.railway.app`
- **Frontend URL**: `https://your-app.vercel.app`
- **Free Limits**: Railway (500 hours/month), Vercel (100GB bandwidth)

Both services offer generous free tiers perfect for your project!