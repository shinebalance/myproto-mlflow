from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

from pprint import pprint
from airflow.operators.python_operator import PythonOperator

"""https://dev.classmethod.jp/articles/airflow-gs-arch-learn/
"""

# Parameters
default_args = {
    'owner': 'hooktack',
    'depends_on_past': False,
    'start_date': days_ago(1),
}
dag = DAG(
    'test_hooktack',
    default_args=default_args,
    description='For TEST execute DAG by hooktack',
    schedule_interval=timedelta(days=1),
)

# BashOperator：date + sleep 5
t1 = BashOperator(
    task_id='getdata',
    bash_command='python /root/airflow-test/mock_getdata.py',
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
    bash_command='python /root/airflow-test/mock_train.py',
    dag=dag,
)

t1 >> t2 >> t3