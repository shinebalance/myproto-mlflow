from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

from pprint import pprint
from airflow.operators.python_operator import PythonOperator


# Parameters
default_args = {
    'owner': 'hooktack',
    'depends_on_past': False,
    'start_date': days_ago(1),
}
dag = DAG(
    'mlproject_run_hooktack',
    default_args=default_args,
    description='データの取得、モデルの訓練、推論を行うワークフロー',
    # schedule_interval=timedelta(minutes=5),
    schedule_interval=timedelta(days=1),
)

# BashOperator：date + sleep 5
t1 = BashOperator(
    task_id='getdata',
    bash_command='cd /opt && pipenv run python scrape/req2url.py',
    dag=dag,
)

t2 = BashOperator(
    task_id='sleep',
    depends_on_past=False,
    bash_command='sleep 5',
    retries=3,
    dag=dag,
)

t3 = BashOperator(
    task_id='train',
    bash_command='cd /opt && pipenv run python mlproject/train_and_predict.py',
    dag=dag,
)

t1 >> t2 >> t3