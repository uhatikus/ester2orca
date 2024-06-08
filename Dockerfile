FROM python:3.10-slim as python-base

# Set work directory
WORKDIR /ester2orca

# Install system dependencies required for psycopg2 compilation
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    # Add any other dependencies your project may need
    && rm -rf /var/lib/apt/lists/*


# Install Poetry
RUN pip3 install poetry && \
    poetry config virtualenvs.create false

# Copy only the dependencies installation files
COPY pyproject.toml poetry.lock* /ester2orca/

# Install dependencies
RUN poetry install --no-root

# Copy the rest of the application
COPY ./ester2orca /ester2orca/ester2orca

# Create a non-root user
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000
# Run the main.py script
CMD ["python", "-m", "uvicorn", "ester2orca.app:app", "--host", "0.0.0.0", "--port", "8000"]