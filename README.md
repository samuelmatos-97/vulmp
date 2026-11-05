# VulMP

VulMP (Vulnerability Management Platform) is a cloud-native DevSecOps project designed to simulate a production-grade vulnerability management platform.

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
* Complete Asset CRUD Operations
* Partial Updates and Request Validation
* HTTP Status Codes and API Documentation
* Database Integration
* Persistent Storage
* Multi-container Application Architecture
* Environment-based Configuration
* Secure Configuration Management
* Dependency Injection
* Database Session Management
* Application Health and Readiness
* Failure and Recovery Testing
* Database Schema Versioning
* Database Migrations and Rollbacks

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
* Alembic

### Testing

* pytest 9.0.2
* FastAPI TestClient
* HTTPX 0.28.1
* Isolated PostgreSQL integration tests

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
* Codex development assistance
* Repository development guidelines in `AGENTS.md`

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

The project currently includes a containerized FastAPI backend integrated with a PostgreSQL database using SQLAlchemy ORM. The backend supports complete Asset CRUD functionality: creation, listing, retrieval by ID, partial updates and deletion.

Application and database configuration is managed through environment variables loaded by Docker Compose.

The development environment includes:

* FastAPI liveness and readiness endpoints
* Native Docker health checks
* PostgreSQL persistent storage
* Database schema versioning with Alembic
* Automatic migration execution before backend startup
* Startup dependency management between PostgreSQL, migrations and the backend

Implemented features:

* FastAPI backend service
* FastAPI lifespan management
* Liveness endpoint
* Readiness endpoint with PostgreSQL validation
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
* Reusable database session dependency
* Automatic database session cleanup
* FastAPI dependency injection with `Depends`
* PostgreSQL Docker health check
* Backend Docker health check
* Backend startup dependency on a healthy PostgreSQL service
* Database migrations with Alembic
* Initial migration for the `assets` table
* Migration upgrade and rollback validation
* Database migration consistency checks
* One-shot Docker migration service
* Backend startup dependency on successful migrations
* Asset creation endpoint
* Asset listing endpoint
* Asset retrieval by ID
* Partial asset updates using explicitly provided fields
* Asset deletion with HTTP `204 No Content`
* Signed 32-bit Asset ID validation
* Rejection of explicit null values in asset updates
* Automatic OpenAPI documentation with optional, non-nullable update fields
* Isolated Docker Compose environment for automated tests
* Test-only configuration and early database destination validation
* Alembic-based test setup and transaction isolation
* Automated CRUD, validation, ID boundary and controlled failure tests

Milestone 8 was validated manually using Swagger UI and `curl`, including persistence, regression, ID boundary, OpenAPI, liveness and readiness checks.

Milestone 9 adds automated API tests using pytest, FastAPI TestClient and an isolated PostgreSQL database. The latest complete local suite result is **62 passed**.

CI/CD pipelines and automated GitHub Actions execution are not yet implemented.

Authentication and authorization are not yet implemented. The API is intended for local development and must not be exposed to untrusted clients without appropriate security controls.

---

## Current Architecture

The diagram and startup flow below describe the development environment. Automated tests use the separate environment described in [Automated API Testing](#automated-api-testing).

```text
Client
  |
  v
FastAPI Backend Container
  |
  |-- GET /health
  |      Checks whether the FastAPI process is alive
  |
  |-- GET /ready
  |      Checks whether PostgreSQL is available
  |
  v
SQLAlchemy ORM
  |
  v
psycopg
  |
  v
PostgreSQL Container
  |
  v
Persistent Docker Volume
```

### Application Startup Flow

```text
Docker Compose
      |
      v
PostgreSQL starts
      |
      v
PostgreSQL becomes healthy
      |
      v
Migration service runs
alembic upgrade head
      |
      v
Migration service exits successfully
      |
      v
FastAPI backend starts
      |
      v
Backend becomes healthy
```

The migration service is a one-shot container. It applies all pending migrations and then exits with status code `0`.

The backend starts only when:

* PostgreSQL is healthy
* All pending database migrations have completed successfully

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

Automated tests use a separate `.env.test` file created from `.env.test.example`. See [Automated API Testing](#automated-api-testing) for the isolated test configuration and commands.

Inside the Docker network, the backend connects to PostgreSQL using:

```text
POSTGRES_HOST=postgres
```

When running database commands directly from the host machine, the hostname must be temporarily changed to:

```text
POSTGRES_HOST=localhost
```

---

## Health and Readiness

The application exposes separate endpoints for liveness and readiness.

### Liveness

```http
GET /health
```

This endpoint confirms that the FastAPI process is running.

Response:

```json
{
  "status": "ok"
}
```

The endpoint does not check external dependencies.

### Readiness

```http
GET /ready
```

This endpoint confirms that the application can communicate with PostgreSQL.

Successful response:

```json
{
  "status": "ready"
}
```

When PostgreSQL is unavailable, the endpoint returns:

```text
503 Service Unavailable
```

Example response:

```json
{
  "detail": "Database unavailable."
}
```

This separation distinguishes between:

* An application process that is alive
* An application that is ready to receive traffic

---

## Docker Health Checks

The PostgreSQL container uses `pg_isready` to verify that the database is accepting connections.

The backend container calls:

```http
GET /ready
```

from inside the container.

The backend is marked as healthy only when:

* The FastAPI process is running
* The readiness endpoint responds successfully
* PostgreSQL is available

If PostgreSQL becomes unavailable after startup:

* The backend process remains alive
* `GET /health` continues returning `200 OK`
* `GET /ready` returns `503 Service Unavailable`
* Docker eventually marks the backend container as `unhealthy`

When PostgreSQL becomes available again, the backend health check recovers automatically without restarting the backend container.

---

## Database Migrations

Alembic is responsible for creating and evolving the PostgreSQL schema.

The FastAPI application no longer creates tables automatically with:

```python
Base.metadata.create_all(bind=engine)
```

Schema changes must now be represented by versioned Alembic migrations.

The initial migration is:

```text
7783a45490f5_create_assets_table.py
```

It creates:

* The `assets` table
* The primary key on `id`
* The `ix_assets_id` index

### Migration Flow

```text
SQLAlchemy models
        |
        v
Alembic migration files
        |
        v
alembic upgrade head
        |
        v
PostgreSQL schema
```

### Alembic Revision States

```text
base
  |
  v
7783a45490f5
  |
  v
head
```

The current database revision is stored in the PostgreSQL table:

```text
alembic_version
```

### Existing Database Baseline

The `assets` table existed before Alembic was introduced.

The existing database was associated with the initial migration using:

```bash
POSTGRES_HOST=localhost \
POSTGRES_DB=vulmp_db \
python -m alembic stamp head
```

The `stamp` command recorded the revision without executing the migration operations, preventing Alembic from attempting to recreate the existing table.

This was a one-time baseline operation and is not required for new installations.

---

## Migration Commands

Run local Alembic commands from:

```bash
cd app/backend
```

Because local commands run outside the Docker network, use `localhost` as the PostgreSQL hostname.

### Show the Current Revision

```bash
POSTGRES_HOST=localhost \
python -m alembic current
```

### Show the Latest Available Revision

```bash
python -m alembic heads
```

### Apply All Pending Migrations

```bash
POSTGRES_HOST=localhost \
python -m alembic upgrade head
```

### Revert the Latest Migration

```bash
POSTGRES_HOST=localhost \
python -m alembic downgrade -1
```

This command reverts only the latest applied migration.

### Revert All Migrations

```bash
POSTGRES_HOST=localhost \
python -m alembic downgrade base
```

This command reverts all applied migrations and returns the database to the state before the first revision.

Downgrades should only be executed in a controlled development environment after reviewing the migration and its impact on stored data.

### Check for Model and Schema Differences

```bash
POSTGRES_HOST=localhost \
python -m alembic check
```

Expected output when the models and database are aligned:

```text
No new upgrade operations detected.
```

### Create a New Migration

After changing an SQLAlchemy model:

```bash
POSTGRES_HOST=localhost \
python -m alembic revision --autogenerate -m "describe schema change"
```

The generated migration must always be reviewed before it is applied.

---

## Docker Migration Service

Docker Compose includes a one-shot service named:

```text
migrate
```

The service runs:

```bash
python -m alembic -c alembic.ini upgrade head
```

The expected service state after startup is:

```text
vulmp-migrate   Exited (0)
```

`Exited (0)` means that all migrations completed successfully.

The complete service state should resemble:

```text
vulmp-postgres   Up (healthy)
vulmp-migrate    Exited (0)
vulmp-backend    Up (healthy)
```

To inspect migration logs:

```bash
docker compose logs migrate
```

To check the current revision inside Docker:

```bash
docker compose run --rm migrate \
  python -m alembic -c alembic.ini current
```

Expected output:

```text
7783a45490f5 (head)
```

To verify that the models and database schema are aligned:

```bash
docker compose run --rm migrate \
  python -m alembic -c alembic.ini check
```

Expected output:

```text
No new upgrade operations detected.
```

---

## Available Endpoints

Asset IDs in the examples are illustrative. Use the actual ID returned by `POST /assets` when making requests. When testing DELETE, create and use a dedicated temporary asset; do not delete existing project data.

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

### Readiness Check

```http
GET /ready
```

Response:

```json
{
  "status": "ready"
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

Successful response: `200 OK`.

```json
{
  "id": 1,
  "name": "web-server-01",
  "asset_type": "server",
  "environment": "production"
}
```

All three string fields are required. Missing fields, invalid field types and explicit null values return HTTP `422`.

---

### List Assets

```http
GET /assets
```

Successful response: `200 OK`.

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

An empty asset collection returns `[]` with HTTP `200 OK`.

---

### Get Asset by ID

```http
GET /assets/{asset_id}
```

Example request: `GET /assets/1`.

Successful response: `200 OK`.

```json
{
  "id": 1,
  "name": "web-server-01",
  "asset_type": "server",
  "environment": "production"
}
```

A missing asset returns `404 Not Found`. Invalid or out-of-range IDs return HTTP `422`, as described below.

---

### Update Asset

```http
PATCH /assets/{asset_id}
```

Example request: `PATCH /assets/1` with the following body:

```json
{
  "environment": "staging"
}
```

Successful response: `200 OK`.

```json
{
  "id": 1,
  "name": "web-server-01",
  "asset_type": "server",
  "environment": "staging"
}
```

The `name`, `asset_type` and `environment` fields are optional to supply. The endpoint applies only explicitly provided fields using:

```python
update_data = asset_update.model_dump(exclude_unset=True)
```

Omitted fields remain unchanged. An empty request object, `{}`, is accepted and leaves the asset unchanged.

Explicit null values, such as `{"environment": null}`, are rejected with HTTP `422` because the database fields are non-nullable. Invalid field types also return HTTP `422`.

`AssetUpdate` uses `str | SkipJsonSchema[None] = None` to allow omitted fields while documenting only string values. The existing field validator rejects explicit null values at runtime; `SkipJsonSchema` controls schema generation only.

A missing asset returns `404 Not Found`. Invalid or out-of-range IDs return HTTP `422`.

---

### Delete Asset

```http
DELETE /assets/{asset_id}
```

Example request: `DELETE /assets/1`.

Use a dedicated temporary asset when testing this endpoint. Deletion permanently removes the matching row after the database transaction is committed.

Successful response:

```http
HTTP/1.1 204 No Content
```

The response body is empty. Subsequent GET or DELETE requests for the same ID return `404 Not Found`.

Invalid or out-of-range IDs return HTTP `422`.

---

### Asset ID Validation and Error Responses

GET, PATCH and DELETE use a shared `AssetId` path parameter type with the inclusive PostgreSQL signed 32-bit `INTEGER` bounds:

* Minimum: `-2147483648`
* Maximum: `2147483647`

Both boundary values are accepted for lookup. Zero and in-range negative IDs also proceed to the normal lookup and return HTTP `404` if no matching asset exists.

Invalid text IDs such as `abc`, fractional values such as `1.5`, and out-of-range values such as `-2147483649` or `2147483648` return HTTP `422` before the endpoint's database lookup executes.

Missing assets return HTTP `404 Not Found` with:

```json
{
  "detail": "Asset not found."
}
```

Validation errors return HTTP `422` with a `detail` array identifying the invalid path parameter or request body field. For example, `GET /assets/2147483648` returns:

```json
{
  "detail": [
    {
      "type": "less_than_equal",
      "loc": ["path", "asset_id"],
      "msg": "Input should be less than or equal to 2147483647",
      "input": "2147483648",
      "ctx": {"le": 2147483647}
    }
  ]
}
```

Database operation errors during PATCH or DELETE trigger rollback of the active transaction and return HTTP `500 Internal Server Error` with `{"detail": "Database operation failed."}`. A completed commit cannot be undone by a later rollback, including when PATCH fails while refreshing the committed asset.

---

## API Documentation

FastAPI automatically generates interactive API documentation.

After starting the application, access:

```text
http://localhost:8000/docs
```

The generated OpenAPI schema is available at:

```text
http://localhost:8000/openapi.json
```

The PATCH request schema documents all three update fields as optional, non-nullable strings. The Asset ID path parameters document the inclusive signed 32-bit bounds. Swagger UI and the generated OpenAPI schema were manually checked during Milestone 8 validation.

---

## Running the Project Locally

### 1. Clone the Repository

```bash
git clone https://github.com/samuelmatos-97/vulmp.git
cd vulmp
```

### 2. Create the Local Environment File

```bash
cp .env.example .env
```

Review the values inside `.env` before proceeding.

### 3. Create a Python Virtual Environment

```bash
py -V:3.12 -m venv .venv
```

### 4. Activate the Virtual Environment Using Git Bash

```bash
source .venv/Scripts/activate
```

### 5. Install Python Dependencies

```bash
python -m pip install -r app/backend/requirements.txt
```

### 6. Validate the Docker Compose Configuration

```bash
docker compose config --quiet
```

No output means that the configuration is valid.

### 7. Build and Start the Environment

```bash
docker compose up --build -d
```

Docker Compose will:

1. Start PostgreSQL
2. Wait for PostgreSQL to become healthy
3. Apply pending Alembic migrations
4. Start the FastAPI backend
5. Begin backend health checks; verify the healthy state in the service checks below

### 8. Check All Service States

```bash
docker compose ps -a
```

Expected state:

```text
vulmp-postgres   Up (healthy)
vulmp-migrate    Exited (0)
vulmp-backend    Up (healthy)
```

### 9. Test the Liveness Endpoint

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

### 10. Test the Readiness Endpoint

Open:

```text
http://localhost:8000/ready
```

Expected response:

```json
{
  "status": "ready"
}
```

### 11. Open the API Documentation

```text
http://localhost:8000/docs
```

### 12. View the Logs

```bash
docker compose logs --tail=50
```

Backend logs only:

```bash
docker compose logs backend --tail=50
```

Migration logs only:

```bash
docker compose logs migrate
```

### 13. Stop the Environment

```bash
docker compose down
```

This removes the containers and Docker network while preserving the PostgreSQL volume and its stored data.

Do not use:

```bash
docker compose down -v
```

unless you intentionally want to delete the PostgreSQL volume and all persisted data.

---

## Automated API Testing

The automated suite uses pytest, FastAPI TestClient and a real PostgreSQL 16 test database. HTTPX provides the HTTP client used by TestClient.

TestClient runs the FastAPI application inside the test runner, including its real lifespan. The development backend and database do not need to be running.

Run the commands below from the repository root using Git Bash. Docker must be running with Linux container support and Docker Compose v2 must support `up --wait`. Installing Python dependencies on the host is not required for this workflow.

Local support for `--wait` remains to be checked during final verification. These setup instructions have not yet been independently validated from a fresh checkout.

### Test Environment Isolation

The test environment is defined in `docker-compose.test.yml` and uses the separate Compose project `vulmp-tests`.

* Both services use a private internal Docker network.
* PostgreSQL has no published host port.
* PostgreSQL stores its data in `tmpfs`, without a persistent database volume.
* Test containers do not mount development data or the Docker socket.
* Local environment files are excluded from Docker build contexts.
* Test configuration uses separate database names, credentials and service names.

The development database and its persistent volume are not part of this test project.

PostgreSQL data remains available while the test database container runs. Stopping that container discards its temporary database storage. The next startup initializes a new database, and pytest prepares its schema through Alembic.

### 1. Configure the Test Environment

For a clean checkout, create the local test configuration:

```bash
cp .env.test.example .env.test
```

Keep an existing `.env.test` file instead of overwriting it.

Open `.env.test` in an editor and configure `TEST_POSTGRES_PASSWORD` with a unique, nonempty test-only password. Never reuse development database credentials or put real credentials in the public template.

Keep the template's database and username unchanged. The safety guard accepts only the approved test destination.

Private `.env` files and their variants are ignored by Git. The public `.env.example` and `.env.test.example` templates remain eligible for tracking.

Every Compose command below explicitly selects:

* `.env.test` for configuration interpolation.
* `vulmp-tests` as the project name.
* `docker-compose.test.yml` as the Compose file.

This avoids relying on automatic loading of the development `.env` file. Exported shell variables take precedence over `--env-file`, so use a shell without conflicting `TEST_POSTGRES_*` values.

### 2. Validate the Compose Configuration

```bash
docker compose --env-file .env.test -p vulmp-tests -f docker-compose.test.yml config --quiet
```

An exit status of `0` indicates a valid configuration.

Use `--quiet` so validation does not print the resolved configuration, which contains the database password.

### 3. Build the Test Image

```bash
docker compose --env-file .env.test -p vulmp-tests -f docker-compose.test.yml build tests
```

`app/backend/Dockerfile.test` uses Python 3.12 and installs `requirements-test.txt`, which includes the existing runtime requirements plus pinned pytest and HTTPX versions.

The image explicitly copies the application, Alembic configuration, migrations and pytest directory. It does not copy local environment files.

### 4. Start the Isolated Test Database

When the test database is not running, start it and wait for its healthcheck:

```bash
docker compose --env-file .env.test -p vulmp-tests -f docker-compose.test.yml up -d --wait postgres-test
```

The test runner also depends on PostgreSQL becoming healthy.

### 5. Run the Complete Suite

```bash
docker compose --env-file .env.test -p vulmp-tests -f docker-compose.test.yml run --rm tests
```

The image's default command runs:

```text
python -m pytest tests
```

The one-time runner container is removed when it exits. PostgreSQL remains running until the test project is stopped.

Latest complete local validation result:

```text
62 passed
```

Run one suite at a time against this Compose project. The current infrastructure is designed for sequential execution.

### 6. Run an Individual Module

For example, run the asset creation and retrieval tests:

```bash
docker compose --env-file .env.test -p vulmp-tests -f docker-compose.test.yml run --rm tests python -m pytest -v tests/test_assets_create_read.py
```

Use paths relative to `/app` inside the image, such as `tests/test_health.py`.

### 7. Rebuild After Changes

The application, migrations, requirements and tests are copied into the image. They are not mounted from the working directory.

After changing copied files or `Dockerfile.test`, rebuild before running tests again:

```bash
docker compose --env-file .env.test -p vulmp-tests -f docker-compose.test.yml build tests
docker compose --env-file .env.test -p vulmp-tests -f docker-compose.test.yml run --rm tests
```

Running an existing image without rebuilding tests the previously copied files.

### 8. Stop the Test Environment

After test execution finishes, stop and remove only the test project's containers and network:

```bash
docker compose --env-file .env.test -p vulmp-tests -f docker-compose.test.yml down
```

This discards the temporary test database storage. The command selects the separate test project and does not target development services or their persistent volume.

No volume-removal option is required.

### Configuration Guards and Database Setup

`tests/conftest.py` validates configuration before test modules import the application. It requires the testing flag, the exact approved PostgreSQL destination and a nonblank password. Previously imported application database modules cause validation to fail.

The session-scoped `test_engine` fixture repeats validation before importing `app.database`. It checks the engine's driver, host, port, database and username before opening a connection. Unexpected URL query parameters or a mismatch with `DATABASE_URL` are rejected.

The fixture loads the existing Alembic configuration using its absolute path and applies `alembic upgrade head` once per pytest execution.

Schema preparation uses the existing migrations. Tests do not use `create_all()`, `drop_all()`, stamping or migration downgrades.

### Transaction Isolation and Cleanup

Each test using the `client` fixture receives a database connection with an outer transaction.

FastAPI's original `get_db` dependency is temporarily overridden. Each request receives a fresh SQLAlchemy session bound to that connection with:

```python
join_transaction_mode="create_savepoint"
```

Endpoint calls to `commit()` operate inside savepoints while the outer test transaction remains active. Requests within the same test can retrieve the assets created by earlier requests.

Request sessions close through context managers. TestClient closes after the test, dependency overrides are restored, and the outer transaction is rolled back before its connection closes. The engine is disposed at the end of the pytest session.

The database setup smoke test uses the validated engine directly and performs read-only checks.

The suite assumes an empty asset collection at the start of each test. Unexpected committed records cause the relevant checks to fail; tests do not automatically delete existing records.

PostgreSQL sequence increments are not rolled back. Tests use IDs returned by the API and do not assume that IDs start at `1`, are sequential, or depend on test execution order.

Changes inside the outer transaction are not globally committed and are not visible through separate connections. The application's lifespan and readiness checks use the validated test engine and only require database connectivity.

### Test Coverage

The nine test modules define 62 cases, including parameterized cases.

| Module under `app/backend/tests/` | Cases | Coverage |
|---|---:|---|
| `test_database_setup.py` | 1 | Database identity, Alembic revision, assets table and index |
| `test_health.py` | 2 | Health and readiness success |
| `test_transaction_isolation.py` | 2 | Isolation between test cases |
| `test_assets_create_read.py` | 5 | Creation, retrieval, collection, empty collection and missing assets |
| `test_assets_update.py` | 5 | Partial updates, omitted fields, empty updates, null rejection and missing assets |
| `test_assets_delete.py` | 3 | Deletion, empty HTTP 204 responses, missing assets and preservation of other assets |
| `test_assets_validation.py` | 23 | Missing/null POST fields and null/invalid-type PATCH fields |
| `test_assets_id_validation.py` | 18 | Valid integer boundaries, out-of-range IDs and malformed IDs |
| `test_assets_database_errors.py` | 3 | PATCH/DELETE commit failures and readiness failure/recovery |
| **Total** | **62** | |

### Controlled Failure Testing Limitations

PATCH and DELETE failure tests exercise the real endpoints and database sessions. They temporarily replace one session's `commit()` with a simulated SQLAlchemy exception and wrap the real `rollback()` method to verify its call.

The simulated exception occurs before the real commit or flush. These tests verify error handling, explicit rollback calls and unchanged asset responses. They do not prove rollback of SQL writes already executed or reversal of a successful commit.

The readiness failure test temporarily replaces only the engine reference used by `app.main`, after TestClient startup. It verifies HTTP 503 during the simulated connection failure and HTTP 200 after restoration.

These simulations do not reproduce a real PostgreSQL outage, network timeout or broken connection pool. Temporary patches are restored before subsequent verification and fixture cleanup.

Automated execution currently runs locally through Docker Compose. CI/CD pipelines and automated GitHub Actions execution remain future work.

---

## Failure and Recovery Test

Stop only PostgreSQL:

```bash
docker compose stop postgres
```

Show both running and stopped services:

```bash
docker compose ps -a
```

Expected behavior:

* PostgreSQL appears as `Exited`
* The backend remains running
* The backend eventually becomes `unhealthy`
* `GET /health` continues responding successfully
* `GET /ready` returns `503 Service Unavailable`

Restart PostgreSQL:

```bash
docker compose start postgres
```

Check the status:

```bash
docker compose ps
```

After PostgreSQL becomes healthy, the backend should also recover and become healthy automatically.

---

## Migration Validation Test

A temporary empty PostgreSQL database was used to validate the initial migration without affecting the main database.

The migration was applied with:

```bash
POSTGRES_HOST=localhost \
POSTGRES_DB=vulmp_migration_test \
python -m alembic upgrade head
```

The migration created:

* The `alembic_version` table
* The `assets` table
* The `ix_assets_id` index

The rollback was tested with:

```bash
POSTGRES_HOST=localhost \
POSTGRES_DB=vulmp_migration_test \
python -m alembic downgrade base
```

This removed the `assets` table and returned the temporary database to the state before the first revision.

The migration was then reapplied with:

```bash
POSTGRES_HOST=localhost \
POSTGRES_DB=vulmp_migration_test \
python -m alembic upgrade head
```

After the validation was completed, the temporary database was removed.

---

## Project Structure

```text
vulmp/
├── app/
│   └── backend/
│       ├── alembic/
│       │   ├── versions/
│       │   │   └── 7783a45490f5_create_assets_table.py
│       │   ├── env.py
│       │   ├── README
│       │   └── script.py.mako
│       ├── app/
│       │   ├── database.py
│       │   ├── main.py
│       │   ├── models.py
│       │   └── schemas.py
│       ├── tests/
│       │   ├── conftest.py
│       │   ├── test_assets_create_read.py
│       │   ├── test_assets_database_errors.py
│       │   ├── test_assets_delete.py
│       │   ├── test_assets_id_validation.py
│       │   ├── test_assets_update.py
│       │   ├── test_assets_validation.py
│       │   ├── test_database_setup.py
│       │   ├── test_health.py
│       │   └── test_transaction_isolation.py
│       ├── alembic.ini
│       ├── Dockerfile
│       ├── Dockerfile.test
│       ├── requirements-test.txt
│       └── requirements.txt
├── .dockerignore
├── .env.example
├── .env.test.example
├── .gitignore
├── AGENTS.md
├── docker-compose.test.yml
├── docker-compose.yml
└── README.md
```

The local `.env` and `.env.test` files are intentionally omitted because they are ignored by Git and must not be committed.

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
* Removed hardcoded database credentials
* Injected environment variables into the backend container
* Built the SQLAlchemy connection URL from environment variables
* Added the reusable `get_db()` database dependency
* Added FastAPI dependency injection with `Depends`
* Added automatic SQLAlchemy session cleanup
* Confirmed that persisted PostgreSQL data remained available

### Milestone 6 — Health, Readiness and Docker Health Checks

* Replaced the deprecated FastAPI startup event with lifespan management
* Added the `GET /ready` endpoint
* Kept `GET /health` as a dedicated liveness endpoint
* Added PostgreSQL connectivity validation to the readiness endpoint
* Added a PostgreSQL Docker health check using `pg_isready`
* Added a backend Docker health check using `GET /ready`
* Configured the backend to wait for a healthy PostgreSQL service
* Tested PostgreSQL service failure
* Confirmed that the backend became unhealthy when PostgreSQL stopped
* Confirmed that liveness remained available during the failure
* Confirmed that readiness returned `503 Service Unavailable`
* Restarted PostgreSQL and validated automatic backend recovery

### Milestone 7 — Database Migrations with Alembic

* Installed and configured Alembic
* Added `python-dotenv` for local migration configuration
* Connected Alembic to the SQLAlchemy models and environment variables
* Created the initial migration for the `assets` table
* Tested the migration upgrade in an empty temporary database
* Tested a complete migration rollback with `downgrade base`
* Reapplied the migration after the rollback
* Removed the temporary migration test database
* Created a baseline for the existing database using `stamp head`
* Preserved the existing PostgreSQL data
* Removed automatic table creation from the FastAPI startup
* Added the Alembic files to the backend Docker image
* Added a one-shot Docker migration service
* Configured the backend to wait for successful migrations
* Validated the current database revision
* Validated that no schema changes were pending
* Confirmed that PostgreSQL and the backend remained healthy

### Milestone 8 — Complete Asset CRUD

* Added `GET /assets/{asset_id}` with the existing HTTP `404` response convention
* Added `PATCH /assets/{asset_id}` for partial updates
* Added `DELETE /assets/{asset_id}` with HTTP `204 No Content` and an empty response body
* Added the `AssetUpdate` schema and explicit null rejection for non-nullable database fields
* Preserved omitted fields using `model_dump(exclude_unset=True)`
* Reused `get_db()`, the existing ORM lookup pattern and `AssetResponse` for retrieval and update responses
* Added commit, refresh and database error rollback handling for updates, and commit and rollback handling for deletion
* Reproduced an HTTP `500` response for an Asset ID above PostgreSQL's signed 32-bit range
* Fixed the ID validation bug with a shared bounded `AssetId` type across GET, PATCH and DELETE
* Corrected the OpenAPI nullable-field mismatch using `SkipJsonSchema[None]` while preserving runtime null rejection
* Used Codex-assisted analysis, incremental implementation, debugging and code review under `AGENTS.md` guidance
* Completed incremental and final read-only code reviews and addressed the identified ID validation and OpenAPI issues
* Manually validated CRUD operations, persistence, omitted fields, null rejection, HTTP `404`/`422` responses and ID boundaries using Swagger UI and `curl`
* Manually validated OpenAPI documentation, regression behavior, `/health` and `/ready`
* Confirmed no blocking issues remained within the agreed local development scope
* Completed the milestone without database schema, dependency or Docker configuration changes

### Milestone 9 — Automated API Testing with pytest

* Added a separate Docker Compose test project with PostgreSQL 16, an internal network and temporary database storage
* Created a dedicated Python 3.12 test image with explicit application, migration and test copies
* Reused runtime requirements and added pinned pytest and HTTPX dependencies
* Added a public test configuration template and strengthened Git and Docker environment-file exclusions
* Implemented early configuration guards and engine destination validation before database access
* Prepared the test schema through the existing Alembic migrations
* Added isolated request sessions using outer transactions, SQLAlchemy savepoints and FastAPI dependency overrides
* Preserved the real application lifespan and restored dependency overrides during cleanup
* Added database setup, health, readiness, CRUD, request validation and Asset ID boundary tests
* Added controlled PATCH/DELETE commit-failure tests and readiness connection-failure recovery testing
* Verified transaction isolation across repeated pytest executions
* Validated the complete local suite with **62 passed**
* Preserved existing application behavior, migrations, runtime requirements and development Docker Compose configuration

Automated execution remains local. CI/CD pipelines and GitHub Actions integration remain future work.

---

## Learning Philosophy

This project is intentionally being developed step-by-step in order to deeply understand each technology, concept and architectural decision involved in modern DevOps and Cloud-Native environments.

The goal is not only to build a working platform, but also to gain practical operational knowledge through troubleshooting, automation, observability and infrastructure design.

Each milestone is implemented incrementally, tested locally, documented and version-controlled using Git and GitHub.

Codex assists with analysis, incremental implementation, debugging and code review following the repository guidelines in `AGENTS.md`. Proposed changes are explained and approved before files are modified. Validation and Git actions remain under user control; commits and pushes require explicit approval.

Codex and `AGENTS.md` support the development workflow. They are not application runtime dependencies or deployed services.

---

## Future Improvements

* Add timestamps to assets
* Improve API error handling
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
