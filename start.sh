set -e

echo "Running database migrations..."
flask db migrate || true
flask db upgrade

echo "Starting production server..."
gunicorn run:app --bind 0.0.0.0:$PORT