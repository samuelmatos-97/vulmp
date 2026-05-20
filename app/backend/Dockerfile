# Uses the official Python 3.12 image as a base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies
COPY app/backend/requirements.txt .

# Install FastAPI/Uvicorn inside the image
RUN pip install --no-cache-dir -r requirements.txt

# Copy the API code
COPY app/backend/app ./app

# Expose the port that the API will run on
EXPOSE 8000

# Runs the FastAPI inside the container
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]
