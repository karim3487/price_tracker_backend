# 📉 Price Tracker Backend

This is a backend service for tracking product prices on marketplaces like Amazon, AliExpress, Costco, etc. Users can
submit product links through a Telegram bot, and the system will monitor the prices and notify them via Telegram and
email when the price drops.

---

## 🚀 Tech Stack

- Django + Django REST Framework
- Celery + Redis
- PostgreSQL
- Scrapy (separate service)
- Aiogram 3 (Telegram bot)
- Docker & Docker Compose

---

## ⚙️ Features

- Product tracking with periodic price checks
- Telegram bot integration for link submission
- Email and Telegram notifications on price drops
- Asynchronous background task queue with Celery
- Scalable architecture (Scrapy as an external service)

---


---

## 🛠️ Installation (Local Development)

### 1. Clone the repository

```bash
git clone https://github.com/karim3487/price_tracker_backend.git
cd price_tracker_backend
```

### 2. Create and activate a virtual environment

```bash
uv init
```

### 3. Install dependencies

```bash
uv install
```

### 4. Configure environment

Create a `.env` file in the root directory:

```
DEBUG=True
SECRET_KEY=your-local-secret-key
CELERY_BROKER_URL=redis://localhost:6379/0
DATABASE_URL=postgres://postgres:postgres@localhost:5443/price_tracker
```

### 5. Run services locally

Make sure Redis and PostgreSQL are running locally, then:

```bash
uv run manage.py makemigrations
uv run manage.py migrate
uv run manage.py runserver
celery -A price_tracker worker --loglevel=info
celery -A price_tracker beat --loglevel=info
```

---

## 🐳 Running with Docker

### 1. Copy `env.example` and rename to `.env.docker`. Refactor them

### 2. Build and run containers

```bash
docker-compose up --build
```

---

## 🔄 Periodic Tasks

The project uses `celery-beat` to periodically check product prices.

- You can configure tasks via Django Admin using `django-celery-beat`
- Or via `CELERY_BEAT_SCHEDULE` in settings

---

## 📬 Webhooks from Scrapy

The external Scrapy service should POST updated price data to:

```
POST /api/price_histories/update_price/
```

Payload example:

```json
{
  "url": "https://example.com/product",
  "price": 89.99
}
```

---

## 📧 Notifications

When a price drop is detected, the system can notify users via:

- Telegram bot
- Email (SMTP settings required, not included in this README)
