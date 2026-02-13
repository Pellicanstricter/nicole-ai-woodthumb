# Nicole FastAPI Application
# Multi-stage Docker build for production deployment

FROM python:3.11-slim as builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY api/ ./api/
COPY knowledge/ ./knowledge/
COPY widget/ ./widget/

# Make sure scripts are in PATH
ENV PATH=/root/.local/bin:$PATH

# Expose port (Railway uses $PORT environment variable)
EXPOSE 8000

# Run application
CMD uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000}
