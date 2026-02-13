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
COPY start.sh ./start.sh

# Make sure scripts are in PATH
ENV PATH=/root/.local/bin:$PATH

# Make start script executable
RUN chmod +x start.sh

# Expose port (Railway uses $PORT environment variable)
EXPOSE 8000

# Run application via shell script (shell form to invoke bash)
CMD /bin/bash ./start.sh
