#!/bin/sh

if [ "$DB_SERVICE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_NAME $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python create_db.py

exec "$@"