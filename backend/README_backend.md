# NaijaCal Backend

Calorie analysis backend for a Nigerian food nutrition application. Users submit a natural language food log and receive a structured calorie breakdown.

---

## What It Does

Takes input like:

```
"I ate 2 cups of beans and 1 wrap of eba"
```

Returns:

```json
{
  "status": "success",
  "data": {
    "items": [
      { "food_name": "beans", "quantity": 2, "unit": "cup", "calories": 508.0 },
      { "food_name": "eba", "quantity": 1, "unit": "wrap", "calories": 952.5 }
    ],
    "total_calories": 1460.5
  }
}
```

---

## Stack

- Python 3.14
- Django 5.0
- Django REST Framework
- SimpleJWT — authentication
- Google Gemini 2.5 Flash — food log parsing
- SQLite (local) / PostgreSQL (production)
- Deployed via Docker + Render

---

## Project Structure

```
backend/
├── api/
│   ├── views/
│   │   ├── auth_views.py       # Register, get current user
│   │   └── meal_views.py       # Submit food log endpoint
│   ├── services/
│   │   ├── analyze_food_log.py # Pipeline orchestrator
│   │   ├── food_interpreter.py # Parses Gemini output into structured items
│   │   └── gemini_service.py   # Gemini API client with key rotation + retries
│   ├── repositories/
│   │   └── food_repository.py  # DB lookup, attaches nutrition data to items
│   ├── domain/
│   │   └── calorie_calculator.py # Converts quantities to grams, calculates calories
│   ├── models.py
│   └── urls.py
└── core/
    └── settings.py
```

---

## Pipeline

```
POST /parse-log
      ↓
meal_views.submit_food_log
      ↓
analyze_food_log          ← orchestrator
      ↓
food_interpreter          ← sends log to Gemini, parses + validates JSON response
      ↓
food_repository           ← queries Food table, attaches calories/grams/unit
      ↓
calorie_calculator        ← computes total_grams per item, calculates kcal
      ↓
JSON response
```

---

## Database

Single table: `api_food`

| Column | Type | Notes |
|---|---|---|
| id | AutoField | Primary key |
| name | CharField(100) | Unique, indexed |
| calories_per_100g | FloatField | kcal per 100g |
| grams_per_unit | FloatField | Weight of the food's default unit in grams |
| default_unit | CharField(50) | e.g. cup, wrap, piece, bowl |

77 Nigerian foods seeded. Calorie formula:

```
total_grams = quantity × grams_per_unit
calories    = (calories_per_100g / 100) × total_grams
```

---

## API Endpoints

### `POST /register`
Register a new user. Returns JWT access and refresh tokens.

**Body:**
```json
{ "username": "seth", "password": "test1234" }
```

**Response:**
```json
{ "refresh": "...", "access": "..." }
```

---

### `POST /api/token/`
Get tokens for an existing user.

**Body:**
```json
{ "username": "seth", "password": "test1234" }
```

---

### `POST /api/token/refresh/`
Refresh an expired access token.

**Body:**
```json
{ "refresh": "<refresh_token>" }
```

---

### `POST /parse-log`
Submit a food log for analysis. Requires authentication.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Body:**
```json
{ "foodLog": "I ate 2 cups of beans and 1 wrap of eba" }
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "items": [
      { "food_name": "beans", "quantity": 2, "unit": "cup", "calories": 508.0 },
      { "food_name": "eba", "quantity": 1, "unit": "wrap", "calories": 952.5 }
    ],
    "total_calories": 1460.5
  }
}
```

---

### `GET /me`
Returns the currently authenticated user's info.

**Headers:**
```
Authorization: Bearer <access_token>
```

---

## Environment Variables

```env
GEMINI_API_KEY_1=your_key_here
GEMINI_API_KEY_2=optional_second_key
GEMINI_API_KEY_3=optional_third_key
SECRET_KEY=django_secret_key
DATABASE_URL=postgres://... (production only)
```

---

## Local Setup

```bash
git clone <repo>
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # fill in your keys
python manage.py migrate
python manage.py runserver
```

---

## Design Principles Applied

- **Separation of Concerns** — each module has one job
- **Single Responsibility** — each file has one reason to change
- **Low Coupling** — calculator knows nothing about Gemini
- **High Cohesion** — all Gemini logic lives only in `gemini_service.py`
- **Explicit Dependencies** — all imports are visible, no hidden globals

---

## Known Gaps / Next Steps

- Duplicate username on register returns 500 (no error handling yet)
- Food alias mapping not implemented ("beans" vs "black-eyed beans")
- No meal history — logs are not persisted per user yet
- Unit conversion for weight-based input ("200g of rice") not handled
