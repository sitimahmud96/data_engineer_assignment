FROM apache/airflow:2.5.0
COPY requirements-airflow.txt /
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements-airflow.txt