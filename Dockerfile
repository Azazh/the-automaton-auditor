# Automaton Auditor Dockerfile
FROM python:3.9-slim

# Set workdir
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy project files
COPY pyproject.toml poetry.lock ./
COPY src ./src
COPY audit ./audit
COPY rubric ./rubric
COPY README.md ./
COPY Makefile ./
COPY .env.example ./

# Install dependencies
RUN poetry install --no-interaction --no-ansi

# Expose environment variables
ENV LANGCHAIN_TRACING_V2=false

# Default command: run audit-self
CMD ["poetry", "run", "audit-self"]
