# v2

This is a full-stack web application with a Python Flask backend and a Vue.js frontend. The project is designed for managing parking reservations and administration, with user authentication, administration interfaces, and background task handling.

## Features

- **User authentication** (JWT-based, Flask-Login support)
- **Administrative dashboard** for managing users, parking lots, and reservations
- **Parking lot and spot management**
- **Reservation system**
- **Email notifications** (SMTP via Flask-Mail)
- **Background job scheduling** with Celery and Redis
- **API** with CORS enabled for the frontend

## Technologies Used

- **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-Login, Flask-JWT-Extended, Flask-Mail, Celery, Redis
- **Frontend:** Vue.js (see `/frontend` directory)
- **Database:** SQLite (default), can be swapped for PostgreSQL/MySQL
- **Task Queue:** Celery with Redis broker
- **Email:** SMTP

---

## Getting Started

### Prerequisites

- Python 3.10+ (recommended)
- Node.js & npm (for the frontend)
- Redis (for Celery)
- [pipenv](https://pipenv.pypa.io/en/latest/) or `virtualenv` (recommended for Python dependency management)

### Backend Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yakitoritrash/v2.git
    cd v2/backend
    ```

2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the `backend` directory with the following (update with your SMTP credentials):

    ```env
    SMTP_SERVER=smtp.example.com
    SMTP_PORT=587
    SMTP_USERNAME=your@email.com
    SMTP_PASSWORD=yourpassword
    ```

5. **Run Database Migrations:**

    ```bash
    flask db upgrade
    ```

6. **Start Redis (if not already running):**

    ```bash
    redis-server
    ```

7. **Run the Flask development server:**

    ```bash
    flask run
    ```

8. **Start Celery worker (in a new terminal):**

    ```bash
    celery -A app.celery_worker.celery worker --loglevel=info
    ```

---

### Frontend Setup

1. **Navigate to the frontend directory:**

    ```bash
    cd ../frontend
    ```

2. **Install dependencies:**

    ```bash
    npm install
    ```

3. **Run the frontend development server:**

    ```bash
    npm run dev
    ```

The frontend will be available at [http://localhost:5173](http://localhost:5173) and will communicate with the backend running at [http://localhost:5000](http://localhost:5000).

---

## Project Structure

```
.
├── backend
│   ├── app/
│   ├── __pycache__/
│   ├── venv/
│   └── ...
├── frontend
│   └── ...
└── README.md
```

- **backend/app/**: Flask application code (models, views, tasks, utils)
- **backend/app/tasks/**: Celery tasks
- **frontend/**: Vue.js frontend

---

## Notes

- Make sure to configure your email (SMTP) settings in `.env` for email notifications to work.
- Default CORS origin is set to `http://localhost:5173` for local Vue.js development.
- By default, the backend uses SQLite (`parking.db`). You can change this in `backend/app/__init__.py` for production.

## License

MIT

---
