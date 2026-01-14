FROM ghcr.io/astral-sh/uv:python3.12-alpine

WORKDIR /app

# Install dependencies
COPY pyproject.toml uv.lock* ./
RUN uv pip install --system --no-cache

# Copy source code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uv", "run", "python", "-m", "app.main"]
