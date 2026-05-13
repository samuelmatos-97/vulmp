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

---

## Current Stack

### Backend
- Python
- FastAPI

### Version Control
- Git
- GitHub

### Development Environment
- Python Virtual Environment (venv)

---

## Planned Technologies

### Cloud
- AWS

### Containerization
- Docker

### Orchestration
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

Initial FastAPI backend with health check endpoint.

Implemented endpoint:

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

## Project Structure

```text
vulmp/
├── app/
│   └── backend/
├── docker-compose.yml
├── README.md
└── .gitignore
```

---

## Learning Philosophy

This project is intentionally being developed step-by-step in order to deeply understand each technology, concept and architectural decision involved in modern DevOps and Cloud-Native environments.

The goal is not only to build a working platform, but also to gain practical operational knowledge through troubleshooting, automation, observability and infrastructure design.

---

## Future Improvements

- Dockerize backend services
- Add PostgreSQL
- Add Redis
- Implement REST APIs
- Create frontend dashboard
- Deploy to Kubernetes
- Implement CI/CD pipelines
- Add monitoring and logging stack
- Apply security scanning and hardening
- Deploy infrastructure to AWS
