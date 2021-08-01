FROM python:3.8-slim-buster
# FROM continuumio/miniconda:4.5.4

RUN pip install --upgrade pip

RUN pip install mlflow \
    && pip install matplotlib \
    && pip install sqlalchemy \
    && pip install sklearn \
    && pip install pandas \
    && pip install cloudpickle

CMD mlflow server --backend-store-uri sqlite:///mlruns/mlruns.sqlite3 --host 0.0.0.0 --default-artifact-root file:mlruns-artifacts/
# CMD mlflow server --backend-store-uri sqlite:///mlruns/mlruns.sqlite3 --host 0.0.0.0 --default-artifact-root artifacts