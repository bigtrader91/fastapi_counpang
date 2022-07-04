import sys

sys.path.append("/home/gumeisbuy/web")
import pandas as pd
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime, timedelta
from dags.utils import SlackAlert




slack = SlackAlert("web")

default_args = {
    "owner": "Daehyeong Lee",
    "depends_on_past": False,
    "email": ["dahy949@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=10),
}

dag_args = dict(
    dag_id="search",
    default_args=default_args,
    description="쿠팡에서 검색 api 사용해서 데이터 수집",
    schedule_interval=timedelta(minutes=8),
    start_date=datetime(2022, 6, 1),
    tags=['검색api'],
    #on_success_callback=slack.success_msg,
    on_failure_callback=slack.fail_msg,
)


def search_add():
    print()



def verify():
    print("검증 완료~")




with DAG(**dag_args) as dag:
    start = BashOperator(
        task_id="start",
        bash_command='echo "start!"',
    )
    chrome = BashOperator(
        task_id="chrome_debugging_mode",
        bash_command='echo "start!"',
    )

    search_api = PythonOperator(task_id="search_add", python_callable=search_add)
    coin_verify = PythonOperator(task_id="verify", python_callable=verify)


    start >> search_api 
    start >> chrome