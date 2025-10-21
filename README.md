# Task Manager

**Task Manager** is a task management system built on Django and Python. It is a web application for organizing, tracking, and managing tasks in a collaborative environment. The system implements user authentication, role-based access control, and flexible task organization using statuses and labels.

## Badges

[![Actions Status](https://github.com/Vitaliy-Berezhnoy/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Vitaliy-Berezhnoy/python-project-52/actions)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Vitaliy-Berezhnoy_python-project-52&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Vitaliy-Berezhnoy_python-project-52)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=Vitaliy-Berezhnoy_python-project-52&metric=coverage)](https://sonarcloud.io/summary/new_code?id=Vitaliy-Berezhnoy_python-project-52)


##  Live Demo

You can try the application right now by following the link: [My project on Render](https://python-project-52-8e31.onrender.com)

**Demo account for login:**
- **Username:** `demo`
- **Password:** `ValidPassword123!`

## 🛠️ Technologies

- **Backend:** Python, Django
- **Frontend:** HTML, Bootstrap (django-bootstrap5)
- **Database:** PostgreSQL
- **Application Server:** Gunicorn
- **Static Files:** Whitenoise
- **Deployment:** Render.com
- **Error Monitoring:** Rollbar
- **Code Quality:** Ruff, SonarCloud
- **CI/CD:** GitHub Actions

## 📋 Features

- **User Management:** Registration, authentication, authorization
- **Task Management:**
  - Create, view, edit, and delete tasks
  - Filter tasks by status, assignee, labels, and other parameters (django-filter)
  - Assign an executor and set a task status
- **Label Management:** Create and manage labels for task categorization
- **Status Management:** Create and manage task statuses (e.g., "New", "In Progress", "Completed")
- **Access Control:** Only authenticated users have access to the application. The author of a task can delete it

## 🛠️ Installation and Setup

### Prerequisites

- Python 3.12 or higher
- The [uv](https://github.com/astral-sh/uv) package manager installed
- PostgreSQL

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Vitaliy-Berezhnoy/python-project-52
   cd python-project-52

2. **Install dependencies**
   ```bash
   make install   

3. **Configure environment variables** 

   Create a .env file in the project root and set the necessary variables, for example: 

   ```bash
   SECRET_KEY=your-secret-key
   DATABASE_URL=postgres://user:password@localhost:5432/db_name
   DEBUG=False

4. **Run database migrations**
   ```bash
   make migrate

5. **Collect static files (for production)**
   ```bash
   make collectstatic

6. **Start the development server**
   ```bash
   make dev

The application will be available at http://127.0.0.1:8000