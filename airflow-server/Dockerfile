FROM python:3.8-slim-buster
# FROM continuumio/miniconda:4.5.4

RUN pip install --upgrade pip

ENV AIRFLOW_HOME=/opt/airflow
RUN pip install "apache-airflow==2.1.2" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.1.2/constraints-3.8.txt"

CMD airflow webserver --port 5005
# CMD mlflow server --backend-store-uri sqlite:///mlruns/mlruns.sqlite3 --host 0.0.0.0 --default-artifact-root file:mlruns-artifacts/