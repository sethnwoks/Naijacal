 # NaijaCal

NaijaCal is a full-stack web app that estimates calories for Nigerian meals from natural-language food logs. A user can type what they ate in plain English, and the app returns a structured breakdown with per-item and total calorie estimates.

The project combines a React frontend, a Django REST API, a curated Nigerian food database, and a Gemini-powered parsing step. It is a practical foundation for a nutrition product focused on local meals rather than generic calorie-tracking workflows.

## What This Project Does

- Accepts a free-form food log such as `"I ate jollof rice and chicken for lunch"`
- Uses Gemini 2.5 Flash to extract structured food items
- Matches those items against a local Nigerian food dataset stored in the database
- Estimates calories per item and totals the full log
- Returns the result through a simple API and frontend UI

## Current Product State

- Anonymous trial mode is the main experience right now.
- `POST /parse-log` is public and rate-limited to 5 requests per IP every 12 hours.
- Authentication endpoints already exist, but auth is disabled by default unless `AUTH_ENABLED=True`.
- Local development falls back to SQLite automatically when `DATABASE_URL` is not set.
- Production deployment is designed around PostgreSQL.

## Example

Input:

```text
Breakfast: 2 slices of bread and 2 eggs
Lunch: Jollof rice and chicken
Dinner: Eba and egusi soup
```

Response shape:

```json
{
  "status": "success",
  "parsed_items": [
    {
      "item": "jollof rice",
      "quantity": 1,
      "unit": "plate",
      "total_calories": 520.0
    }
  ],
  "total_calories": 520.0,
  "remaining_trials": 4
}
```

The exact breakdown depends on the AI parse and whether each food exists in the local database.

## Core Features

- Natural-language calorie logging for Nigerian meals
- Curated database of 100+ food entries
- AI parsing backed by Gemini API key rotation across up to 3 keys
- Clear separation between parsing, nutrition lookup, and calorie calculation
- React frontend for quick manual use
- JWT auth endpoints with refresh-cookie support when auth is enabled
- Docker Compose setup for local full-stack development

## Tech Stack

### Backend

- Django 5
- Django REST Framework
- SimpleJWT
- Google Gemini 2.5 Flash
- SQLite for local fallback
- PostgreSQL for deployment

### Frontend

- React 19
- Create React App
- Plain CSS

### Infrastructure

- Docker and Docker Compose
- Render-oriented deployment flow

## How It Works

```text
React frontend
    ->
POST /parse-log
    ->
meal_views.submit_food_log
    ->
rate_limit_service.check_anonymous_parse_limit
    ->
analyze_food_log
    ->
food_interpreter
    ->
gemini_service
    ->
food_repository.attach_nutrition
    ->
calorie_calculator.calculate_calories
    ->
JSON response
```

If a parsed food item does not exist in the database, the item is still returned, but its calorie value comes back as `null`.

## Project Structure

```text
Health_App/
├── backend/
│   ├── api/
│   │   ├── domain/                  # Calorie calculation logic
│   │   ├── management/commands/     # Food seeding and data utilities
│   │   ├── repositories/            # Database lookup layer
│   │   ├── services/                # AI parsing and orchestration
│   │   └── views/                   # API endpoints
│   ├── core/                        # Django settings and URL config
│   ├── .env.example
│   └── manage.py
├── frontend/
│   └── frontend/
│       ├── public/
│       ├── src/
│       ├── .env.example
│       └── package.json
├── docker-compose.yml
├── DEPLOY.md
└── README.md
```

## Local Setup

Python 3.11 and Node.js 20 are the safest choices if you want to match the Docker setup in this repo.

### 1. Clone the repository

```bash
git clone https://github.com/sethnwoks/Health_App.git
cd Health_App
```

### 2. Start the backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `backend/.env` and set at least:

```env
GEMINI_API_KEY_1=your_gemini_key_here
DEBUG=True
AUTH_ENABLED=False
```

Then run:

```bash
python manage.py migrate
python manage.py populate_foods
python manage.py runserver
```

The backend will be available at `http://localhost:8000`.

### 3. Start the frontend

Open a second terminal:

```bash
cd frontend/frontend
npm install
cp .env.example .env
npm start
```

By default the frontend expects:

```env
REACT_APP_API_URL=http://localhost:8000
```

The frontend will be available at `http://localhost:3000`.

## Docker Setup

If you want to run the full stack with Docker:

```bash
cp backend/.env.example backend/.env
cp frontend/frontend/.env.example frontend/frontend/.env
docker compose up --build
```

Then initialize the backend data:

```bash
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py populate_foods
```

Notes:

- Set `GEMINI_API_KEY_1` in `backend/.env` before starting.
- The Django settings currently read `DATABASE_URL` for PostgreSQL. If you want Django to use the Postgres container from [`docker-compose.yml`](./docker-compose.yml), point `DATABASE_URL` to that service.
- If `DATABASE_URL` is left unset, Django falls back to SQLite.

## Environment Variables

### Backend

| Variable | Required | Purpose |
|---|---|---|
| `GEMINI_API_KEY_1` | Yes | Primary Gemini API key |
| `GEMINI_API_KEY_2` | No | Secondary fallback key |
| `GEMINI_API_KEY_3` | No | Tertiary fallback key |
| `DEBUG` | Recommended | Controls Django debug mode |
| `SECRET_KEY` | Recommended in all environments | Django secret key |
| `AUTH_ENABLED` | No | Enables registration and JWT auth flows |
| `DATABASE_URL` | No for local, yes for hosted Postgres | Database connection string |
| `ALLOWED_HOSTS` | No | Django allowed hosts |
| `CORS_ALLOWED_ORIGINS` | No | Frontend origins allowed by the API |

### Frontend

| Variable | Required | Purpose |
|---|---|---|
| `REACT_APP_API_URL` | Yes | Base URL for the Django API |

## API Overview

### Public endpoint

| Endpoint | Method | Description |
|---|---|---|
| `/parse-log` | `POST` | Parse a food log and return calorie estimates |

Example request:

```bash
curl -X POST http://localhost:8000/parse-log \
  -H "Content-Type: application/json" \
  -d '{"foodLog":"I ate jollof rice and chicken"}'
```

### Auth-related endpoints

These endpoints are implemented, but they return `503` unless `AUTH_ENABLED=True`.

| Endpoint | Method | Description |
|---|---|---|
| `/register` | `POST` | Create a new user |
| `/api/token/` | `POST` | Obtain access token |
| `/api/token/refresh/` | `POST` | Refresh access token using cookie-backed refresh token |
| `/logout` | `POST` | Invalidate refresh token and clear cookie |
| `/me` | `GET` | Return the current authenticated user |

## Data Seeding

The app needs the `Food` table populated before calorie estimation becomes useful.

Use:

```bash
python manage.py populate_foods
```

There are also supporting utilities in `backend/api/management/commands/` for extracting and updating the food dataset.

## Known Limitations

- Authentication exists in code, but anonymous trial mode is the default experience today.
- Calorie estimates depend on the quality of the AI parse and the coverage of the local food database.
- Unknown foods are returned without calorie values instead of being auto-enriched from an external nutrition source.
- Unit conversion is based on simple defaults and generic gram mappings.
- Automated test coverage is still minimal.

## Deployment

Deployment notes live in [`DEPLOY.md`](./DEPLOY.md).

The project is structured for:

- Django backend deployment on Render
- React frontend deployment from `frontend/frontend`
- PostgreSQL in hosted environments

## Repository Notes

- The backend has an additional engineering-focused document at [`backend/README_backend.md`](./backend/README_backend.md).
- The frontend subdirectory still contains the default Create React App README, but the main project guide is this file.

## License

This repository includes a [`LICENSE`](./LICENSE) file.
