FROM python:3.14-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Enable bytecode compilation and copy lockfiles first for caching
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Copying the project files
COPY pyproject.toml uv.lock ./

# Install dependencies without installing the project itself
RUN uv sync --frozen --no-install-project

# Copy the rest of the application
COPY . .

# Final sync to install the project
RUN uv sync --frozen

# Place /app/.venv/bin at the beginning of PATH
ENV PATH="/app/.venv/bin:$PATH"

#TODO CHANGE THIS
CMD ["python", "main.py"]