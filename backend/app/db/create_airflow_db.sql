-- Create the airflow user if it doesn't exist
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'airflow') THEN
      CREATE USER "airflow" WITH PASSWORD 'root';
   END IF;
END
$do$;

-- Grant necessary permissions
ALTER USER "airflow" WITH SUPERUSER;

-- Create dblink extension
CREATE EXTENSION IF NOT EXISTS dblink;

-- Create airflow database if it doesn't exist
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_database
      WHERE datname = 'airflow') THEN
      PERFORM dblink_exec('dbname=' || current_database(),
         'CREATE DATABASE airflow');
   END IF;
END
$do$;

-- Grant privileges to airflow user
GRANT ALL PRIVILEGES ON DATABASE airflow TO "airflow";
GRANT ALL PRIVILEGES ON DATABASE etl_sentimentify TO "airflow";

-- Grant schema permissions
\c airflow;
GRANT ALL ON SCHEMA public TO "airflow";
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "airflow";
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO "airflow";

\c etl_sentimentify;
GRANT ALL ON SCHEMA public TO "airflow";
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "airflow";
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO "airflow";
