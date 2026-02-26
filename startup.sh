#!/bin/bash
# Azure Web App Startup Script

echo "=== Starting FABLE Game Server ==="
echo "Python version: $(python3 --version)"
echo "Working directory: $(pwd)"

# Install gunicorn if not present
if ! python3 -m pip show gunicorn > /dev/null 2>&1; then
    echo "Installing gunicorn..."
    python3 -m pip install gunicorn
fi

# Navigate to backend directory
if [ -d "backend" ]; then
    cd backend
    echo "Changed to backend directory: $(pwd)"
else
    echo "Warning: backend directory not found, assuming flat structure"
fi

# Start the FastAPI server with Gunicorn
echo "Starting Gunicorn on port ${PORT:-8000}..."
exec python3 -m gunicorn app.main:app \
    --worker-class uvicorn.workers.UvicornWorker \
    --workers 2 \
    --bind 0.0.0.0:${PORT:-8000} \
    --timeout 600 \
    --access-logfile - \
    --error-logfile - \
    --log-level info