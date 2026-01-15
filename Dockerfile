# Multi-stage build for optimized image size
FROM python:3.11-slim as builder

# Install system dependencies needed for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Verify celery is installed (helps catch issues early)
RUN python -c "import celery; print(f'Celery version: {celery.__version__}')" || (echo "ERROR: Celery installation failed" && exit 1)

# Final stage
FROM python:3.11-slim

# Install runtime system dependencies
# poppler-utils is needed for pdf2image
# libglib2.0-0 is needed for image processing libraries
# libgl1 is needed for OpenCV (replaces libgl1-mesa-glx in newer Debian)
# libgthread-2.0-0 is needed for OpenCV threading
RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    libglib2.0-0 \
    libgl1 \
    libgthread-2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app && \
    chown -R appuser:appuser /app

# Set working directory
WORKDIR /app

# Copy Python packages from builder stage
# Use --chown to ensure proper ownership
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Add local bin to PATH and ensure Python can find user-installed packages
ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONPATH=/home/appuser/.local/lib/python3.11/site-packages:$PYTHONPATH

# Verify critical packages are accessible (celery, fastapi, uvicorn)
RUN python -c "import celery, fastapi, uvicorn; print('✓ All critical packages imported successfully')" || \
    (echo "ERROR: Failed to import critical packages. Check installation." && exit 1)

# Expose port
EXPOSE 5002

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5002/api/v1/health', timeout=5)" || exit 1

# Run the application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "5002"]

