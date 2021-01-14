#!/bin/bash
set -e

cd /app

migrate_and_run () {

    # echo "Waiting for postgres..."

    # while ! nc -z $DB_HOST $DB_PORT; do
    # sleep 0.1
    # done

    # echo "PostgreSQL started"

    echo "======== MIGRATING ========"
    python manage.py migrate --noinput
    echo "======== RUNNING APP ========"
    exec "$@"
}

migrate_and_run "$@"
