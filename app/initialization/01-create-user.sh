#!/bin/bash

# =====================================================
# Strict Mode Flags:
#   -e: Exit immediately if any command exits with non-zero status
#   -u: Treat unset variables as an error
# =====================================================
set -eu

# Wait for PostgreSQL server to be ready before proceeding
# pg_isready checks if PostgreSQL is accepting connections
until pg_isready -U "$POSTGRES_USER"; do
  sleep 1
done

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Create dedicated application user (non-superuser for security)
    CREATE USER "$POSTGRESQL_USERNAME" WITH PASSWORD '$POSTGRESQL_PASSWORD';
    
    -- Create application database
    CREATE DATABASE "$POSTGRESQL_DB_NAME";
    
    -- Grant all privileges on the created database (not on the entire server) to application user
    GRANT ALL PRIVILEGES ON DATABASE "$POSTGRESQL_DB_NAME" TO "$POSTGRESQL_USERNAME";
    
    -- Make application user the owner of the database
    ALTER DATABASE "$POSTGRESQL_DB_NAME" OWNER TO "$POSTGRESQL_USERNAME";
EOSQL
