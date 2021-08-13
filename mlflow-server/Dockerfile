FROM python:3.8-slim-buster
# FROM continuumio/miniconda:4.5.4

RUN pip install --upgrade pip

RUN pip install mlflow==1.19.0 \
    && pip install matplotlib==3.4.2 \
    && pip install sqlalchemy==1.4.22 \
    && pip install scikit-learn==0.24.2 \
    && pip install pandas==1.3.1 \
    && pip install cloudpickle==1.6.0

CMD mlflow server --backend-store-uri sqlite:///mlruns/mlruns.sqlite3 --host 0.0.0.0 --default-artifact-root file:mlruns-artifacts/
# CMD mlflow server --backend-store-uri sqlite:///mlruns/mlruns.sqlite3 --host 0.0.0.0 --default-artifact-root artifacts