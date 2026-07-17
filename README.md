# 🎯 InterviewPilot

> A backend-first AI interview platform built with **FastAPI**, designed to streamline technical interview preparation through secure authentication, interview management, and scalable REST APIs.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?logo=postgresql)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00)
![JWT](https://img.shields.io/badge/JWT-Authentication-black?logo=jsonwebtokens)
![OAuth2](https://img.shields.io/badge/OAuth2-Authorization-blue)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI-2088FF?logo=githubactions)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📖 Overview

InterviewPilot is a backend application that powers an AI-driven mock interview platform. It provides secure user authentication, interview management APIs, and a scalable backend architecture that will later integrate AI-generated interview questions and personalized feedback.

The project follows RESTful API principles using FastAPI and is designed with modularity, scalability, and maintainability in mind.

> **Note:** AI-powered interview generation is currently under development and will be integrated in a future release.

---

## ✨ Features

### Authentication

- JWT Authentication
- OAuth2 Authentication
- Secure Login & Registration
- Protected API Endpoints

### Interview Management

- Create Interviews
- Retrieve Interview Details
- Update Interview Information
- Delete Interviews
- Manage Interview Sessions

### API

- RESTful API Design
- Request Validation using Pydantic
- Interactive API Documentation
- Modular Route Organization
- Environment-based Configuration

### Development

- PostgreSQL Database
- SQLAlchemy ORM
- GitHub Actions CI
- Docker & Docker Compose
- Postman API Testing
- Clean Project Structure

---

## 🛠 Tech Stack

| Category | Technologies |
|-----------|--------------|
| Language | Python |
| Backend Framework | FastAPI |
| Authentication | JWT, OAuth2 |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Data Validation | Pydantic |
| API Documentation | Swagger UI |
| Testing | Postman |
| CI | GitHub Actions |
| Version Control | Git, GitHub |
| Environment Management | python-dotenv |

---

## 📂 Project Structure

```text
InterviewPilot/
│
├── 
├── agents/
├── audio_analyser/
├── audio_extractor/
├── database/
├── models/
├── routers/
├── schemas/
├── services/
├── utils/
├── orchestrator/
├── postman/
├── security/
├── .dockerignore
├── .gitignore
├── Dockerfile
├── docker-compose.yml
│
├── .github/
│   └── workflows/
│
├── requirements.txt
├── .env
├── app.py
└── README.md
```

---

## 🚀 Getting Started

## Option 1 - Run locally

### 1. Clone the Repository

```bash
git clone https://github.com/SLokesh1810/InterviewPilot.git

cd InterviewPilot
```

---

### 2. Create a Virtual Environment

**Windows**

```bash
python -m venv venv

venv\Scripts\activate
```

**Linux/macOS**

```bash
python3 -m venv venv

source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file in the project root.

Example:

```env
GOOGLE_API_KEY="YOUR_API_KEY"

# Testing variable
USE_LLM = 'false' # If you have API key then switch it to true

# Audio storage
BASE_PATH="YOUR_BASE_PATH"

FFMPEG_PATH="FFMPEG_LOCATION"

# Database - Test
DATABASE_URL="YOUR_DB_URL"

SECRET_KEY="SECRET_KEY"
```

> Add any additional environment variables required by your local setup.

---

### 5. Run the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

---

## 🐳 Option 2 – Run with Docker

### Prerequisites

- Docker
- Docker Compose

### 1. Clone the Repository

```bash
git clone https://github.com/SLokesh1810/InterviewPilot.git

cd InterviewPilot
```

### 2. Configure Environment Variables

Create a `.env` file in the project root and update the required environment variables.

### 3. Build the Docker Images

```bash
docker compose build
```

### 4. Start the Containers

```bash
docker compose up
```

or run in detached mode

```bash
docker compose up -d
```

### 5. Stop the Containers

```bash
docker compose down
```

The API will be available at

```
http://localhost:8000
```

Swagger UI

```
http://localhost:8000/docs
```

---

## 📚 API Documentation

FastAPI automatically generates interactive API documentation.

| Documentation | URL |
|--------------|-----|
| Swagger UI | `/docs` |

Example:

```
http://127.0.0.1:8000/docs
```

---

## 🔒 Authentication

InterviewPilot secures protected endpoints using:

- JSON Web Tokens (JWT)
- OAuth2 Authentication Flow
- Bearer Token Authorization

---

## 🗄 Database

The project uses **PostgreSQL** as its primary database.

Database interactions are handled through **SQLAlchemy ORM**, providing clean and maintainable database operations.

---

## 🧪 API Testing

API endpoints are tested using **Postman**.

The project includes requests for:

- User Registration
- User Login
- Protected Endpoints
- Interview CRUD Operations
- Authentication Testing

---

## ⚙ Continuous Integration

GitHub Actions is configured to automate project workflows, helping ensure code quality and consistency during development.

---

## 🔮 Roadmap

### Current

- ✅ FastAPI Backend
- ✅ JWT Authentication
- ✅ OAuth2 Authentication
- ✅ PostgreSQL Integration
- ✅ Interview CRUD APIs
- ✅ API Documentation
- ✅ GitHub Actions CI

### Planned

- 🔄 AI Interview Question Generation
- 🔄 AI-Based Interview Feedback
- 🔄 Alembic Database Migrations
- 🔄 Resume Upload
- 🔄 Resume Analysis
- 🔄 Email Verification
- 🔄 Password Reset
- 🔄 Frontend Application
- 🔄 Deployment
- 🔄 Comprehensive Automated Testing

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Lokesh S**

- GitHub: https://github.com/SLokesh1810

---

## ⭐ Support

If you found this project helpful, consider giving it a ⭐ on GitHub!