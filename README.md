# VulMP

VulMP (Vulnerability Management Platform) is a cloud-native DevSecOps project designed to simulate a production-like vulnerability management platform.

The main goal of this project is to learn and apply modern DevOps, DevSecOps, Cloud and Platform Engineering practices by building a realistic distributed environment from scratch.

---

## Project Goals

This project aims to provide hands-on experience with:

* Cloud Infrastructure
* Docker and Containerization
* Kubernetes Orchestration
* CI/CD Pipelines
* Infrastructure as Code (IaC)
* Monitoring and Observability
* Logging and Alerting
* Networking Concepts
* Security Scanning and Hardening
* Linux and Automation
* Backend API Development
* Database Integration
* Persistent Storage
* Multi-container Application Architecture
* Environment-based Configuration
* Secure Configuration Management
* Dependency Injection
* Database Session Management

---

## Current Stack

### Backend

* Python 3.12
* FastAPI
* Pydantic
* SQLAlchemy
* psycopg

### Database

* PostgreSQL 16

### Version Control

* Git
* GitHub

### Containerization

* Docker
* Docker Compose

### Development Environment

* Python Virtual Environment (`venv`)
* Visual Studio Code
* Git Bash

---

## Planned Technologies

### Cloud

* AWS

### Container Orchestration

* Kubernetes

### Infrastructure as Code

* Terraform

### Configuration Management

* Ansible

### CI/CD

* GitHub Actions

### Monitoring and Observability

* Prometheus
* Grafana
* Loki
* Alertmanager

### Security

* Bandit
* Trivy
* Checkov
* Kubernetes RBAC
* Network Policies

---

## Current Status

The project currently includes a containerized FastAPI backend integrated with a PostgreSQL database using SQLAlchemy ORM.

Application and database configuration is managed through environment variables loaded by Docker Compose.

Implemented features:

* FastAPI backend service
* Health check endpoint
* Dockerized backend application
* Docker Compose multi-service environment
* PostgreSQL database container
* Persistent PostgreSQL Docker volume
* SQLAlchemy database integration
* PostgreSQL connection using psycopg
* Environment-based database configuration
* Local `.env` configuration
* Public `.env.example` configuration template
* Protection of local environment variables through `.gitignore`
* Safe SQLAlchemy connection URL construction
* Automatic database table creation
* Reusable database session dependency
* Automatic database session cleanup
* FastAPI dependency injection with `Depends`
* Asset creation endpoint
* Asset listing endpoint
* Automatic OpenAPI documentation

---

## Current Architecture

```text
.env
  ↓
Docker Compose
  ├── FastAPI Backend Container
  │       ↓
  │   SQLAlchemy ORM
  │       ↓
  │    psycopg
  │       ↓
  └── PostgreSQL Container
          ↓
     Docker Volume
```

The current environment runs locally using Docker Compose.

Docker Compose currently manages:

* `backend` service
* `postgres` service
* Internal Docker network
* Persistent PostgreSQL volume
* Environment variable injection

The backend and PostgreSQL containers communicate through the internal Docker network by using the PostgreSQL service name as the database hostname.

---

## Configuration Management

Local application configuration is stored in:

```text
.env
```

This file contains local environment values and is excluded from Git through `.gitignore`.

A public configuration template is available in:

```text
.env.example
```

After cloning the repository, create the local environment file with:

```bash
cp .env.example .env
```

Review and update the values before starting the application.

The currently required variables are:

```env
POSTGRES_USER=vulmp
POSTGRES_PASSWORD=replace_with_a_secure_password
POSTGRES_DB=vulmp_db
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
```

The `.env` file must never be committed to the repository.

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

### 2. Create the local environment file

```bash
cp .env.example .env
```

Review the values inside `.env` before proceeding.

### 3. Create a Python virtual environment

```bash
py -V:3.12 -m venv .venv
```

### 4. Activate the virtual environment using Git Bash

```bash
source .venv/Scripts/activate
```

### 5. Install Python dependencies

```bash
pip install -r app/backend/requirements.txt
```

### 6. Validate the Docker Compose configuration

```bash
docker compose config --quiet
```

No output means that the configuration is valid.

### 7. Run the application with Docker Compose

```bash
docker compose up --build
```

### 8. Test the health endpoint

Open:

```text
http://localhost:8000/health
```

Expected response:

```json
{
  "status": "ok"
}
```

### 9. Open the API documentation

```text
http://localhost:8000/docs
```

### 10. Stop the environment

```bash
docker compose down
```

This removes the containers and Docker network while preserving the PostgreSQL volume and its stored data.

Do not use `docker compose down -v` unless you intentionally want to delete the PostgreSQL volume and all persisted data.

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
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
```

The local `.env` file is intentionally excluded from this structure because it is not committed to Git.

---

## Implemented Milestones

### Milestone 1 — Project Foundation

* Created the initial project structure
* Configured the local development environment
* Initialized the Git repository
* Created the GitHub repository
* Added the initial project documentation

### Milestone 2 — FastAPI Backend Foundation

* Created the initial FastAPI application
* Added the `/health` endpoint
* Configured the Python virtual environment
* Installed the initial dependencies
* Validated local backend execution

### Milestone 3 — Dockerization

* Created the backend Dockerfile
* Built the Docker image
* Ran the FastAPI backend inside a Docker container
* Added Docker Compose support
* Validated the containerized `/health` endpoint

### Milestone 4 — PostgreSQL Integration

* Added the PostgreSQL service to Docker Compose
* Created a persistent PostgreSQL volume
* Integrated FastAPI with PostgreSQL using SQLAlchemy and psycopg
* Created the initial `Asset` ORM model
* Created the database table automatically
* Added the `POST /assets` endpoint
* Added the `GET /assets` endpoint
* Validated persistent data across container restarts

### Milestone 5 — Configuration and Database Session Management

* Created local `.env` configuration
* Created a public `.env.example` template
* Protected `.env` through `.gitignore`
* Removed hardcoded database credentials from the Python code
* Removed hardcoded PostgreSQL values from Docker Compose
* Injected environment variables into the backend container
* Built the SQLAlchemy connection URL from environment variables
* Added the reusable `get_db()` database dependency
* Added FastAPI dependency injection with `Depends`
* Added automatic SQLAlchemy session cleanup
* Validated the existing `GET /assets` endpoint
* Validated the existing `POST /assets` endpoint
* Confirmed that persisted PostgreSQL data remained available

---

## Learning Philosophy

This project is intentionally being developed step-by-step in order to deeply understand each technology, concept and architectural decision involved in modern DevOps and cloud-native environments.

The goal is not only to build a working platform, but also to gain practical operational knowledge through troubleshooting, automation, observability and infrastructure design.

Each milestone is implemented incrementally, tested locally, documented and version-controlled using Git and GitHub.

---

## Future Improvements

* Add separate liveness and readiness endpoints
* Add Docker health checks
* Replace deprecated FastAPI startup events with lifespan management
* Add Alembic database migrations
* Add full CRUD operations for assets
* Add asset retrieval by ID
* Add asset update and deletion endpoints
* Add vulnerability and scan models
* Add frontend dashboard
* Add authentication and authorization
* Add CI/CD pipelines with GitHub Actions
* Add SAST and container image scanning
* Add Kubernetes manifests
* Add Helm chart
* Add monitoring with Prometheus and Grafana
* Add logging with Loki
* Deploy infrastructure to AWS using Terraform
