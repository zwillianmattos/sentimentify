FROM apache/airflow:2.7.1-python3.9

USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy initialization script and set permissions
COPY init-airflow.sh /init-airflow.sh
RUN chmod +x /init-airflow.sh

USER airflow

# Copy requirements and install Python packages
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

# Copy application code
COPY ./app /usr/src/app

# Copy DAGs to the airflow dags folder
COPY ./dags /opt/airflow/dags

# Create DAGs folder (not needed anymore since we're copying the dags directory)

EXPOSE 5432

ENTRYPOINT ["/init-airflow.sh"]