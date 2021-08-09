FROM python:3.8-slim-buster
# FROM continuumio/miniconda:4.5.4

RUN pip install --upgrade pip

# Airflow実行環境
ENV AIRFLOW_HOME=/opt/airflow
RUN pip install "apache-airflow==2.1.2" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.1.2/constraints-3.8.txt"

# mlproject実行環境
RUN pip install pipenv
WORKDIR /opt/
COPY Pipfile .
RUN pipenv install
# 各種フォルダの配置
RUN mkdir logs
RUN mkdir data
# mlproject実行時に表示されるgitログの省略
RUN export GIT_PYTHON_REFRESH=quiet

# Airflow webserver実行
CMD airflow webserver --port 5005
# CMD mlflow server --backend-store-uri sqlite:///mlruns/mlruns.sqlite3 --host 0.0.0.0 --default-artifact-root file:mlruns-artifacts/