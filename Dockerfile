# Use base image from GitHub Container Registry
FROM ghcr.io/plantoncloud-inc/backend/services/graph-fleet:base-latest

WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install Poetry and dependencies only (skip project package)
RUN pip install --no-cache-dir poetry==1.8.5 && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-root --no-interaction --no-ansi

# Copy application code
COPY . .

# Now install the project package itself
RUN poetry install --no-dev --only-root --no-interaction --no-ansi

# Create directory for state persistence
RUN mkdir -p /app/.langgraph

# Expose port 8080 (following Planton Cloud convention)
EXPOSE 8080

# Run langgraph dev (no license required)
CMD ["poetry", "run", "langgraph", "dev", "--host", "0.0.0.0", "--port", "8080"]

