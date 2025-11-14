#!/bin/bash
set -e

# Fix permissions for mounted volumes (run as root)
if [ -d "/app/staticfiles" ]; then
    chown -R appuser:appuser /app/staticfiles || true
    chmod -R 755 /app/staticfiles || true
fi

if [ -d "/app/media" ]; then
    chown -R appuser:appuser /app/media || true
    chmod -R 755 /app/media || true
fi

# Switch to appuser and execute the command
exec gosu appuser "$@"

