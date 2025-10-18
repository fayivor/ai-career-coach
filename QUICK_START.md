# AI Career Coach - Quick Start Guide

## What is this?

AI Career Coach is a full-stack web application that uses AI to help with career development:
- Chat with an AI career coach
- Analyze your resume with AI
- Find skill gaps for target jobs
- Get personalized course recommendations
- Track your career goals

## Fastest Way to Run

### Option 1: Docker (Recommended - 2 minutes)

```bash
# Navigate to project
cd ai-career-coach

# Start everything
docker-compose up --build

# Wait 2-5 minutes for AI models to download (first time only)
```

Then open:
- **App**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

### Option 2: Local Development (5 minutes)

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend (in new terminal):**
```bash
cd frontend
npm install
npm run dev
```

## Using the App

### 1. Chatbot
- Navigate to Chatbot page
- Ask career questions like:
  - "How do I prepare for a software engineering interview?"
  - "What skills should I learn for data science?"
  - "How do I negotiate salary?"

### 2. Resume Analyzer
- Upload your resume (PDF or DOCX)
- Get AI-powered summary
- See extracted skills, experience, and education
- Identify key entities

### 3. Skill Gap Analysis
- Enter your current skills (comma-separated)
- Select target job role
- See which skills you're missing
- Get percentage match
- Receive recommendations

### 4. Course Recommendations
- Browse all available courses
- Filter by level (Beginner/Intermediate/Advanced)
- See courses for specific skills
- Get direct links to course providers

### 5. Goal Tracker
- Create career goals with deadlines
- Track progress (Pending/In Progress/Completed)
- View statistics
- Update or delete goals

## Available Job Roles

The system supports skill gap analysis for:
- Software Engineer
- Data Scientist
- Frontend Developer
- Backend Developer
- Fullstack Developer
- DevOps Engineer
- ML Engineer

## Sample Data to Try

### Sample Skills
```
Python, JavaScript, React, SQL, Git
```

### Sample Target Role
```
Software Engineer
```

### Sample Career Questions
- "What certifications should I get for cloud computing?"
- "How can I transition from frontend to fullstack development?"
- "What's the difference between a software engineer and a data scientist?"

## Troubleshooting

### Models Taking Too Long
- First startup downloads ~2GB of AI models
- Subsequent starts are much faster
- Models are cached in Docker volumes

### Port Already in Use
```bash
# Change ports in docker-compose.yml
# Frontend: change "3000:80" to "3001:80"
# Backend: change "8000:8000" to "8001:8000"
```

### Frontend Can't Connect to Backend
- Make sure both containers are running: `docker-compose ps`
- Check backend logs: `docker-compose logs backend`
- Verify health: http://localhost:8000/health

## Next Steps

1. **Test the API**: Visit http://localhost:8000/docs for interactive API documentation
2. **Customize**: Modify course recommendations in `backend/app/services/course_recommender.py`
3. **Add Roles**: Add more job roles in `backend/app/routers/skills.py`
4. **Deploy**: Follow README.md for deployment instructions
5. **Contribute**: See README.md for contribution guidelines

## Stopping the App

```bash
# Stop all containers
docker-compose down

# Stop and remove volumes (fresh start next time)
docker-compose down -v
```

## Tech Stack Quick Reference

- **Backend**: FastAPI + Hugging Face Transformers
- **Frontend**: React + Vite + TailwindCSS
- **Database**: SQLite
- **AI Models**: DialoGPT, BART, BERT, Sentence Transformers
- **Deployment**: Docker + Docker Compose + GitHub Actions

## Support

- Check [README.md](README.md) for full documentation
- View API docs at http://localhost:8000/docs
- Open GitHub issue for bugs/features

---

**Happy Career Coaching!**
