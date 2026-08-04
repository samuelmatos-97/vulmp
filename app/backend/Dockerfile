# Use a lightweight Python 3.12 base image.
FROM python:3.12-slim

# Set the working directory inside the container.
WORKDIR /app

# Copy and install the Python dependencies first.
# This allows Docker to reuse the dependency layer when only code changes.
COPY app/backend/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Copy the Alembic configuration and migration files.
COPY app/backend/alembic.ini ./alembic.ini
COPY app/backend/alembic ./alembic

# Copy the FastAPI application code.
COPY app/backend/app ./app

# Document the port used by the FastAPI application.
EXPOSE 8000

# Start the API when the backend container runs.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
