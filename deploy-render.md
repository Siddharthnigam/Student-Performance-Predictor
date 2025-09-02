# Deploy to Render (Free)

## 🚀 Backend Deployment

1. **Go to [render.com](https://render.com)**
2. **Sign up with GitHub**
3. **New Web Service**:
   - Connect your GitHub repo
   - **Root Directory**: Leave empty
   - **Build Command**: `cd echopredict_backend && pip install -r requirements.txt`
   - **Start Command**: `cd echopredict_backend && python manage.py migrate && python manage.py collectstatic --noinput && gunicorn echopredict_backend.wsgi:application`

4. **Environment Variables**:
   - `DEBUG`: `False`
   - `SECRET_KEY`: (auto-generated)
   - `DATABASE_URL`: (auto-provided by PostgreSQL)

5. **Add PostgreSQL Database**:
   - In dashboard, click "New" → "PostgreSQL"
   - Name: `echopredict-db`

## 🌐 Frontend (Vercel)

Same as before - deploy `echopredict_frontend` folder to Vercel.

## ✅ Benefits
- Free PostgreSQL database
- Automatic HTTPS
- Easy deployment from GitHub