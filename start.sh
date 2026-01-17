#!/bin/bash

# Startup script for the Nebula Proxy

echo "🚀 Starting Nebula Proxy..."

# Check if config file exists, if not copy example
if [ ! -f /app/config/proxies.json ]; then
    echo "📝 Creating default config from example..."
    cp /app/config/proxies.example.json /app/config/proxies.json
fi

# Start the FastAPI server
echo "✅ Starting FastAPI server on port 8000..."
exec uvicorn backend.main:app --host 0.0.0.0 --port 8000
