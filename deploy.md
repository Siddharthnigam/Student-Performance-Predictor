# EchoPredict Deployment Guide

## Quick Local Deployment

### Option 1: Docker (Recommended)
```bash
docker-compose up --build
```
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

### Option 2: Manual Setup
```bash
# Backend
cd echopredict_backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Frontend (new terminal)
cd echopredict_frontend
npm install
npm run dev
```

## Cloud Deployment

### Heroku
1. Install Heroku CLI
2. `heroku create your-app-name`
3. `git add . && git commit -m "Deploy"`
4. `heroku git:remote -a your-app-name`
5. `git push heroku main`

### Vercel (Frontend only)
1. `cd echopredict_frontend`
2. `npm run build`
3. Deploy to Vercel

### AWS/DigitalOcean
Use the Docker setup with your preferred cloud provider.

## Environment Variables
- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to False in production
- `DATABASE_URL`: Database connection string