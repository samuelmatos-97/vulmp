# VulMP

VulMP (Vulnerability Management Platform) is a cloud-native DevSecOps project designed to simulate a production-grade vulnerability management platform.

The main goal of this project is to learn and apply modern DevOps, DevSecOps, Cloud and Platform Engineering practices by building a realistic distributed environment from scratch.

---

## Project Goals

This project aims to provide hands-on experience with:

- Cloud Infrastructure
- Docker and Containerization
- Kubernetes Orchestration
- CI/CD Pipelines
- Infrastructure as Code (IaC)
- Monitoring and Observability
- Logging and Alerting
- Networking Concepts
- Security Scanning and Hardening
- Linux and Automation
- Backend API Development
- Database Integration
- Persistent Storage
- Multi-container Application Architecture

---

## Current Stack

### Backend
- Python 3.12
- FastAPI
- Pydantic
- SQLAlchemy

### Database
- PostgreSQL 16

### Version Control
- Git
- GitHub

### Containerization
- Docker
- Docker Compose

### Development Environment
- Python Virtual Environment (venv)
- VS Code
- Git Bash

---

## Planned Technologies

### Cloud
- AWS

### Container Orchestration
- Kubernetes

### Infrastructure as Code
- Terraform

### Configuration Management
- Ansible

### CI/CD
- GitHub Actions

### Monitoring & Observability
- Prometheus
- Grafana
- Loki
- Alertmanager

### Security
- Bandit
- Trivy
- Checkov
- Kubernetes RBAC
- Network Policies

---

## Current Status

The project currently includes a containerized FastAPI backend integrated with a PostgreSQL database using SQLAlchemy ORM.

Implemented features:

- FastAPI backend service
- Health check endpoint
- Dockerized backend application
- Docker Compose multi-service environment
- PostgreSQL database container
- Persistent PostgreSQL Docker volume
- SQLAlchemy database connection
- Automatic database table creation
- Asset creation endpoint
- Asset listing endpoint
- Automatic OpenAPI documentation

---

## Current Architecture

```text
Browser / API Client
        ↓
FastAPI Backend Container
        ↓
SQLAlchemy ORM
        ↓
PostgreSQL Container
        ↓
Docker Volume
```

The current environment runs locally using Docker Compose.

Docker Compose currently manages:

- `backend` service
- `postgres` service
- internal Docker network
- persistent PostgreSQL volume

---

## Available Endpoints

### Health Check

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

---

### Create Asset

```http
POST /assets
```

Example request body:

```json
{
  "name": "web-server-01",
  "asset_type": "server",
  "environment": "production"
}
```

Example response:

```json
{
  "id": 1,
  "name": "web-server-01",
  "asset_type": "server",
  "environment": "production"
}
```

---

### List Assets

```http
GET /assets
```

Example response:

```json
[
  {
    "id": 1,
    "name": "web-server-01",
    "asset_type": "server",
    "environment": "production"
  }
]
```

---

## API Documentation

FastAPI automatically generates interactive API documentation.

After starting the application, access:

```text
http://localhost:8000/docs
```

---

## Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/samuelmatos-97/vulmp.git
cd vulmp
```

### 2. Create a Python virtual environment

```bash
py -V:3.12 -m venv .venv
```

### 3. Activate the virtual environment using Git Bash

```bash
source .venv/Scripts/activate
```

### 4. Install Python dependencies

```bash
pip install -r app/backend/requirements.txt
```

### 5. Run the application with Docker Compose

```bash
docker compose up --build
```

### 6. Test the health endpoint

```text
http://localhost:8000/health
```

Expected response:

```json
{
  "status": "ok"
}
```

---

## Project Structure

```text
vulmp/
├── app/
│   └── backend/
│       ├── app/
│       │   ├── database.py
│       │   ├── main.py
│       │   ├── models.py
│       │   └── schemas.py
│       ├── Dockerfile
│       └── requirements.txt
├── docker-compose.yml
├── README.md
└── .gitignore
```

---

## Implemented Milestones

### Milestone 1 — Project Foundation

- Created initial project structure
- Configured local development environment
- Initialized Git repository
- Created GitHub repository
- Added initial project documentation

### Milestone 2 — FastAPI Backend Foundation

- Created initial FastAPI application
- Added `/health` endpoint
- Configured Python virtual environment
- Installed initial dependencies
- Validated local backend execution

### Milestone 3 — Dockerization

- Created backend Dockerfile
- Built Docker image
- Ran FastAPI backend inside a Docker container
- Added Docker Compose support
- Validated containerized `/health` endpoint

### Milestone 4 — PostgreSQL Integration

- Added PostgreSQL service to Docker Compose
- Created persistent PostgreSQL volume
- Integrated FastAPI with PostgreSQL using SQLAlchemy and psycopg
- Created initial `Asset` ORM model
- Created database table automatically
- Added `POST /assets` endpoint
- Added `GET /assets` endpoint
- Validated persistent data across container restarts

---

## Learning Philosophy

This project is intentionally being developed step-by-step in order to deeply understand each technology, concept and architectural decision involved in modern DevOps and Cloud-Native environments.

The goal is not only to build a working platform, but also to gain practical operational knowledge through troubleshooting, automation, observability and infrastructure design.

Each milestone is implemented incrementally, tested locally, documented and version-controlled using Git and GitHub.

---

## Future Improvements

- Move configuration to environment variables
- Add `.env` support
- Improve database session management
- Add dependency injection for database sessions
- Add Alembic database migrations
- Add full CRUD operations for assets
- Add vulnerability and scan models
- Add frontend dashboard
- Add authentication and authorization
- Add CI/CD pipelines with GitHub Actions
- Add SAST and container image scanning
- Add Kubernetes manifests
- Add Helm chart
- Add monitoring with Prometheus and Grafana
- Add logging with Loki
- Deploy infrastructure to AWS using Terraform
