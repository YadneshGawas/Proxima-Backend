set -e

echo "Running database migrations..."
flask db migrate || true
flask db upgrade

echo "Starting Flask application..."
python run.py
