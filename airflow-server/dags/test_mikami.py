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
    'owner': 'ec2-user',
    'depends_on_past': False,
    'start_date': days_ago(2),
}
dag = DAG(
    'test_mikami',
    default_args=default_args,
    description='For TEST execute DAG',
    schedule_interval=timedelta(days=1),
)

# BashOperator：date + sleep 5
t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag,
)

t2 = BashOperator(
    task_id='sleep',
    depends_on_past=False,
    bash_command='sleep 5',
    retries=3,
    dag=dag,
)

# PythonOperator：print
def print_context(ds, **kwargs):
    pprint(kwargs)
    print(ds)
    return 'Hello! Airflow!!'


run_this = PythonOperator(
    task_id='print_the_context',
    provide_context=True,
    python_callable=print_context,
    dag=dag,
)

t1 >> t2 >> run_this