import datetime
import os

from omegaconf import OmegaConf
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator


dag_script_path = os.path.dirname(os.path.abspath(__file__))
config_dir_path = os.path.join(dag_script_path, "config")

# read variables config
config = OmegaConf.load(os.path.join(config_dir_path, "variables.yaml"))

# region DAG

# default dag arguments
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime.datetime(2021, 1, 1),
    "email": config.email,
    "retries": 0
}

dag = DAG(
    "brazilian-e-commerce-etl",
    default_args=default_args,
    description="Brazilian E-Commerce ETL DAG",
    catchup=False,
    schedule_interval="0 9 * * *",  # everyday at 09:00 UTC
    tags=["Brazilian E-Commerce", "etl"],
    default_view="graph",
    max_active_runs=1,
)

# generate dag documentation
dag.doc_md = __doc__

# endregion
task_list = []
def createDynamicETL(table_name):
    task = BashOperator(
        task_id=table_name,
        bash_command=config.read_write_command + " --table_name {{ params.table_name }}",
        params={'table_name' : table_name},
        dag=dag
    )
    return task

etl_start = DummyOperator(task_id="etl_start", dag=dag)
completed = DummyOperator(task_id="completed", dag=dag)
etl_end = DummyOperator(task_id="etl_end", dag=dag)

missed_orders = BashOperator(
        task_id="missed_orders",
        bash_command=config.missed_orders_command,
        dag=dag
    )

for table_name in config["tables"]:
    task_list.append(createDynamicETL(table_name))

for i in range(len(task_list)):
    etl_start >> task_list[i] >> completed
completed >> missed_orders >> etl_end