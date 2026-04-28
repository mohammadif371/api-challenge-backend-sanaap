#!/bin/bash
set -e

echo "Waiting for PostgreSQL..."
python << END
import socket
import time

while True:
    try:
        sock = socket.create_connection(("db", 5432), timeout=1)
        sock.close()
        print("PostgreSQL is ready!")
        break
    except (socket.error, OSError):
        print("Waiting...")
        time.sleep(1)
END

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server..."
exec "$@"
