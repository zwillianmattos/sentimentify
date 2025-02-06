FROM apache/airflow:2.7.1-python3.9

USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Copy requirements and install Python packages
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

# Copy application code
COPY ./app /usr/src/app

# Create DAGs folder
RUN mkdir -p /opt/airflow/dags

EXPOSE 5432

CMD ["python", "./etl_script.py"]