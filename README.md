# Student Management System

A simple cloud-ready Student Management System built with Flask and PostgreSQL.

## Features
- Add student
- View student records
- Edit student
- Delete student
- PostgreSQL database
- Health-check endpoint
- Ready for Render deployment

## Technologies
- Python
- Flask
- PostgreSQL
- HTML/CSS
- GitHub
- Render

## Local setup

1. Install Python 3.
2. Create a PostgreSQL database.
3. Set the `DATABASE_URL` environment variable.
4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Run:

```bash
python app.py
```

6. Open `http://127.0.0.1:5000`

## Cloud deployment

The project includes `render.yaml`. You can also create a Render Web Service from the GitHub repository with:

Build command:
`pip install -r requirements.txt`

Start command:
`gunicorn app:app`

Set `DATABASE_URL` to the PostgreSQL connection string.
