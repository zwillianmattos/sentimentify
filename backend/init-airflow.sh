#!/bin/bash
set -e

# Wait for PostgreSQL to be ready
until PGPASSWORD=root psql -h postgres -U airflow -d airflow -c '\q'; do
  >&2 echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

>&2 echo "PostgreSQL is up - executing Airflow initialization"

# Initialize Airflow
airflow db init

# Create admin user if it doesn't exist
airflow users list | grep -q "admin" || \
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin

# Start the service based on the command
case "$1" in
  "webserver")
    exec airflow webserver
    ;;
  "scheduler")
    exec airflow scheduler
    ;;
  *)
    exec "$@"
    ;;
esac 