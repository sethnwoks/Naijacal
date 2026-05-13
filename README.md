# 🥘 NaijaCal: AI-Powered Nigerian Nutrition Platform

[![CI Pipeline](https://github.com/sethnwoks/NaijaCal/actions/workflows/ci.yml/badge.svg)](https://github.com/sethnwoks/NaijaCal/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

### 🚀 [Live Demo: NaijaCal Platform](https://naijacal-frontend.onrender.com)

📖 **Overview**  
NaijaCal is a production-grade health application designed to bridge the gap in nutritional tracking for West African cuisine. Using Gemini 1.5 Flash and a curated database of Nigerian foods, it interprets natural language logs (e.g., *"I had 2 wraps of eba and a bowl of egusi"*) and provides instant, accurate caloric breakdowns.

---

## ✨ Features
- 🧠 **AI-Powered Parsing**: Real-time natural language processing using Google Gemini.
- 🍲 **Culturally Relevant**: Specifically tuned for Nigerian portion sizes and traditional meals (Swallow, Soups, Proteins).
- 🛡️ **Production Hardened**: Built with HSTS, secure cookie headers, and JWT-ready architecture.
- 🔄 **High Availability**: Custom AI Key Rotation service to maximize uptime on free-tier limits.
- ⚡ **Full-Stack Performance**: React frontend with a clean, modern UI and a Django REST backend.

---

## 📦 Technologies
- **Backend**: Python 3.11, Django 5.0+, Django REST Framework.
- **AI Engine**: Google Gemini 1.5 Flash (via `google-genai` SDK).
- **Frontend**: React.js, Vanilla CSS (Premium Design).
- **Database**: PostgreSQL (Production), SQLite (Development).
- **Infrastructure**: Docker, Docker Compose, Render Blueprints.
- **Testing**: Pytest, Pytest-Django, Pytest-Cov.

---

## 🗂️ Repository Structure

```bash
.
├── backend/                # Django REST API
│   ├── api/                # Core business logic
│   │   ├── services/       # AI Interpretation & Key Rotation logic
│   │   ├── repositories/   # Clean Data Access Layer (DAL)
│   │   └── views/          # API Endpoints & Request Handling
│   ├── core/               # Main settings & URL routing
│   ├── tests/              # Full Testing Pyramid (Unit, Integration, Security)
│   └── requirements.txt    # Managed production dependencies
├── frontend/               # React Application
│   └── frontend/           # Source code & UI Components
├── .github/workflows/      # CI/CD Pipeline (GitHub Actions)
├── docker-compose.yml      # Local development orchestration
└── render.yaml             # Production Infrastructure-as-Code (Blueprint)
```

---

## 🔗 Architecture Flow

```mermaid
graph TD
    User((User)) -->|Food Log Text| React[React Frontend]
    React -->|POST /parse-log| Django[Django API]
    Django -->|Analyze Text| AI_Service[Gemini AI Service]
    AI_Service -->|Rotate Key| Keys[(API Key Pool)]
    AI_Service -->|Structured JSON| Django
    Django -->|Enrich Nutrition| DB[(PostgreSQL)]
    DB -->|Caloric Data| Django
    Django -->|Final Results| React
    React -->|Display Results| User
```

---

## ✅ Requirements & Installation

### 🔧 Configuration
Create a `.env` file in the `backend/` directory based on `.env.example`:
```env
SECRET_KEY=your-secure-key
GEMINI_API_KEY_1=your-api-key
DATABASE_URL=postgres://user:pass@localhost:5432/db
```

### 🚀 Local Setup (Docker)
The easiest way to run the project is via Docker:
```bash
docker-compose up --build
```
The app will be available at `http://localhost:3000`.

### 🧪 Running Tests
We maintain 90%+ coverage on core business logic:
```bash
cd backend
pytest --cov=api tests/
```

---

## 🤝 Contributing
Guidelines for contributing:
1. Fork the project.
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the Branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📝 Changelog
- **deploy**: add auto-seeding for Nigerian food database (12 minutes ago)
- **fix**: implement universal failover for all AI service errors (19 minutes ago)
- **deploy**: fix CORS and API URL protocol for Render (36 minutes ago)
- **ui**: remove trial mode subtitle (42 minutes ago)
- **deploy**: loosen dependency versions for better compatibility (59 minutes ago)
- **fix**: resolve requirements.txt syntax error for CI (75 minutes ago)
- **deploy**: add render blueprint and final testing updates (81 minutes ago)

---

## ❤️ Acknowledgements
- Built with ❤️ by **Seth N.** as part of a high-performance portfolio.
- Food data curated from traditional Nigerian nutritional benchmarks.
- Special thanks to the Google DeepMind team for the Gemini API.

---

📄 **License**  
Distributed under the MIT License. See `LICENSE` for more information.
