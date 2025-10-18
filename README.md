# AI Career Coach

A full-stack AI-powered career coaching platform that helps users chat with an AI coach, upload resumes for analysis, identify skill gaps, and get personalized course recommendations.

## Features

- **AI Chatbot**: Chat with an AI career coach powered by OpenAI GPT-3.5-turbo
  - Real-time conversational AI with memory
  - Personalized career guidance and recommendations
  - Context-aware responses using conversation history
- **Resume Analyzer**: Upload PDF/DOCX resumes for AI-powered analysis
- **Skill Gap Analysis**: Compare your skills against target job roles
- **Course Recommendations**: Get personalized course suggestions based on skill gaps
- **Goal Tracker**: Track and manage your career development goals

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **OpenAI GPT-3.5-turbo**: Conversational AI for chatbot
- **Hugging Face Transformers**: AI/ML models
  - BART for text summarization
  - BERT for named entity recognition
  - Sentence Transformers for skill matching
- **SQLite**: Database for goal tracking
- **pytest**: Testing framework

### Frontend
- **React 18**: UI library
- **Vite**: Build tool
- **TailwindCSS**: Styling
- **React Router**: Navigation
- **Axios**: API client
- **React Icons**: Icon library

### DevOps
- **Docker & Docker Compose**: Containerization
- **GitHub Actions**: CI/CD pipeline
- **Nginx**: Frontend server

## Project Structure

```
ai-career-coach/
├── backend/
│   ├── app/
│   │   ├── routers/          # API endpoints
│   │   │   ├── chatbot.py
│   │   │   ├── resume.py
│   │   │   ├── skills.py
│   │   │   ├── recommend.py
│   │   │   └── tracker.py
│   │   ├── services/         # Business logic
│   │   │   ├── ai_models.py
│   │   │   ├── resume_processor.py
│   │   │   └── course_recommender.py
│   │   ├── models/           # Data models
│   │   │   ├── schemas.py
│   │   │   └── database.py
│   │   └── main.py           # FastAPI app
│   ├── tests/                # Backend tests
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── pages/            # React pages
│   │   │   ├── ChatbotPage.jsx
│   │   │   ├── ResumeAnalyzerPage.jsx
│   │   │   ├── SkillGapPage.jsx
│   │   │   ├── RecommendationsPage.jsx
│   │   │   └── TrackerPage.jsx
│   │   ├── services/         # API client
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── Dockerfile
│   └── nginx.conf
├── .github/
│   └── workflows/
│       └── ci-cd.yml         # CI/CD pipeline
├── docker-compose.yml
└── README.md
```

## Quick Start

### Prerequisites
- Docker and Docker Compose
- OR Python 3.11+ and Node.js 18+ (for local development)

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone <your-repo-url>
cd ai-career-coach
```

2. Build and run with Docker Compose:
```bash
docker-compose up --build
```

3. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Local Development

#### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the backend:
```bash
uvicorn app.main:app --reload
```

Backend will be available at http://localhost:8000

#### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

Frontend will be available at http://localhost:3000

## API Endpoints

### Chatbot
- `POST /api/chatbot/chat` - Send message to AI coach
- `GET /api/chatbot/health` - Check chatbot status

### Resume
- `POST /api/resume/analyze` - Upload and analyze resume (PDF/DOCX)
- `GET /api/resume/health` - Check analyzer status

### Skills
- `POST /api/skills/gap-analysis` - Analyze skill gap
- `GET /api/skills/roles` - Get available job roles
- `GET /api/skills/role/{role_name}` - Get role requirements

### Recommendations
- `POST /api/recommendations/courses` - Get course recommendations
- `GET /api/recommendations/courses/all` - Get all courses
- `GET /api/recommendations/courses/provider/{provider}` - Filter by provider
- `GET /api/recommendations/courses/level/{level}` - Filter by level

### Tracker
- `POST /api/tracker/goals` - Create new goal
- `GET /api/tracker/goals` - Get all goals
- `GET /api/tracker/goals/{goal_id}` - Get specific goal
- `PUT /api/tracker/goals/{goal_id}` - Update goal
- `DELETE /api/tracker/goals/{goal_id}` - Delete goal
- `GET /api/tracker/stats` - Get tracker statistics

## Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Backend Linting
```bash
cd backend
flake8 app
```

### Frontend Build
```bash
cd frontend
npm run build
```

## CI/CD

The project includes a GitHub Actions workflow that:
1. Runs backend tests and linting (pytest, flake8)
2. Runs frontend linting and build
3. Builds Docker images
4. Tests Docker containers
5. Ready for deployment (configure your deployment target)

## Deployment

### Option 1: Docker Deployment

Deploy the entire stack using Docker Compose on any cloud provider:
- AWS EC2
- DigitalOcean Droplet
- Google Cloud Compute Engine

### Option 2: Separate Deployment

**Backend (FastAPI)**:
- Render
- Railway
- Google Cloud Run
- AWS ECS

**Frontend (React)**:
- Vercel
- Netlify
- AWS S3 + CloudFront

## Environment Variables

### Backend
- `OPENAI_API_KEY`: Your OpenAI API key for GPT-3.5-turbo (required for chatbot)
- `DATABASE_URL`: Database connection string (default: SQLite)

See `backend/.env.example` for a template.

### Frontend
- `VITE_API_URL`: Backend API URL (default: http://localhost:8000)

## AI Models Used

1. **OpenAI GPT-3.5-turbo**: Conversational AI for chatbot with context memory
2. **facebook/bart-large-cnn**: Text summarization for resumes
3. **dslim/bert-base-NER**: Named entity recognition
4. **sentence-transformers/all-MiniLM-L6-v2**: Semantic similarity for skill matching

## Performance Considerations

- First startup may take 2-5 minutes as AI models are downloaded
- Models are cached after first download
- Resume analysis: ~5-10 seconds per document
- Chatbot response: ~1-3 seconds per message (GPT-3.5-turbo)
- Skill gap analysis: ~1-2 seconds
- OpenAI API costs: ~$0.002 per conversation (very affordable)

## Future Enhancements

- [ ] User authentication and profiles
- [ ] Resume version tracking
- [ ] Job posting integration
- [ ] Interview preparation module
- [ ] Career path visualization
- [ ] Email notifications for goal deadlines
- [ ] Social sharing features
- [ ] Mobile app

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

MIT License

## Support

For issues and questions, please open a GitHub issue.

---

Built with FastAPI, React, Hugging Face, and Docker
