FROM apache/airflow:2.8.1-python3.10

USER airflow

# Cài thêm thư viện cần thiết
RUN pip install --no-cache-dir \
    pandas \
    scikit-learn \
    joblib \
    psycopg2-binary \
    requests

USER airflow
