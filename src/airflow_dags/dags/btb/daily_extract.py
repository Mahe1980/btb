from pathlib import Path
from datetime import datetime, timedelta
from src.core.service.ctl_service import CTLService
from src.core.service.extractor import Extractor
from src.settings import envs
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.operators.dummy_operator import DummyOperator
import gzip
import shutil
import json
import os
import logging
from src.settings import log_config

# Setting up module from __file__ as the interpreter sets __name__ as __main__ when the source file is executed as
# main program
logger = logging.getLogger(name=__file__.replace(envs.PROJECT_ROOT, '').replace('/', '.')[1:-3])

# these args will get passed on to each operator
# you can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email': ['airflow@airflow.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
    'catchup': False
}

DAG_ID = '{p.parent.name}_{p.stem}'.format(p=Path(__file__))
PARAMS = Variable.get(DAG_ID, deserialize_json=True)

SCOPE = PARAMS['scope']
FREQUENCY = PARAMS['frequency']
JSON_OUTPUT_FOLDER = PARAMS['json_output_folder']
DELTA_OUTPUT_FOLDER = PARAMS['delta_output_folder']
SOURCE_NAMES = PARAMS['source_names']
SCHEDULE_INTERVAL = PARAMS.get('schedule_interval') or None
HWM = PARAMS.get("hwm", dict())
output_dir = "{}/{}".format(envs.PROJECT_ROOT, JSON_OUTPUT_FOLDER)
remote_push = PARAMS.get("remote_push", False)


dag = DAG(
    DAG_ID,
    default_args=default_args,
    description='BT Bill Daily Extract',
    schedule_interval=SCHEDULE_INTERVAL,
    dagrun_timeout=timedelta(minutes=PARAMS.get('dag_timeout_min')),
    max_active_runs=1
)


def get_cutoff_ts(current_time):
    unit = HWM.get("unit", "hours")
    value = HWM.get("value", 2)

    if unit == "hours":
        td = timedelta(hours=value)
    elif unit == "days":
        td = timedelta(days=value)
    else:
        td = timedelta(hours=2)  # default is 2 hours

    return current_time - td


def run_extract(source_name, **context):
    logger.info("Extracting data for table '{}'".format(source_name))

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_time = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")
    cutoff_ts = get_cutoff_ts(current_time)
    output_file = "{}/{}.json".format(output_dir, "{}_{}_delta".format(source_name, cutoff_ts.strftime("%Y%m%d%H%M%S")))
    path = Path(output_file)
    if path.is_file():
        path.unlink()
    ctl_obj = CTLService(SCOPE, FREQUENCY, source_name)
    ctl_source = ctl_obj.get_sources()[0]
    field = 'state'
    ctl_obj.update_field(field, "running")
    try:
        Extractor(ctl_source, cutoff_ts).run(output_file)
    except Exception as e:
        logger.error("Data Extraction Failed for {}".format(source_name))
        logger.error(e)
        ctl_obj.update_field(field, 'failed')
        raise
    else:
        ctl_obj.update_field(field, 'completed')
        ctl_obj.update_field("last_success_ts", current_time)
    finally:
        ctl_obj.update_field("last_run_ts", current_time)

    logger.info("Extracted data for table '{}'".format(source_name))
    task_instance = context['task_instance']
    task_instance.xcom_push(key="cutoff_ts", value=cutoff_ts)
    task_instance.xcom_push(key="output_file", value=output_file)


def create_extract_task(source_name):
    return PythonOperator(
        task_id='extract_{}'.format(source_name),
        python_callable=run_extract,
        provide_context=True,
        op_kwargs={"source_name": source_name},
        dag=dag)


def move_file(source_name, **context):
    json_output_path = context['ti'].xcom_pull(task_ids='extract_{}'.format(source_name), key="output_file")
    if not json_output_path:
        logger.info("No file to process")
        return
    path = Path(json_output_path)
    logger.info("Gzipping and moving file {} from tmp to delta dir".format(path.name))
    delta_output_path = "{}/{}/{}.gz".format(envs.PROJECT_ROOT, DELTA_OUTPUT_FOLDER, path.name)
    with open(json_output_path, 'rb') as f_in, gzip.open(delta_output_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    Path(json_output_path).unlink()
    logger.info("Gzipped and moved file {} from tmp to delta dir".format(path.name))


def file_mover(source_name):
    return PythonOperator(
        task_id='move_{}'.format(source_name),
        python_callable=move_file,
        op_kwargs={"source_name": source_name},
        provide_context=True,
        dag=dag)


def hwm_update(source_name, **context):
    cutoff_ts = context['ti'].xcom_pull(task_ids='extract_{}'.format(source_name), key='cutoff_ts')
    ctl_obj = CTLService(SCOPE, FREQUENCY, source_name)
    ctl_source = ctl_obj.get_sources()[0]
    value = json.loads(ctl_source.value)
    value["HWM1"] = cutoff_ts.strftime("%Y-%m-%d %H:%M:%S")
    value = json.dumps(value)
    ctl_obj.update_field("value", value)
    logger.info("Updated watermark column for '{}'".format(source_name))


def update_wm(source_name):
    return PythonOperator(
        task_id='watermark_{}'.format(source_name),
        python_callable=hwm_update,
        op_kwargs={"source_name": source_name},
        provide_context=True,
        dag=dag)


def start_up():
    try:
        logger.info("cleaning up tmp dir {}".format(output_dir))
        [p.unlink() for p in Path(output_dir).glob('*')]
    except Exception as e:
        logger.error(e)
        raise Exception(e)

    ctl_sources = CTLService(SCOPE, FREQUENCY).get_sources()
    source_names = [ctl_source.source_name for ctl_source in ctl_sources]
    if set(source_names) != set(SOURCE_NAMES):
        logger.error("Source names not matching with Airflow variable and Oracle GCP_MIGRATION_TABLE.")
        logger.error("Updating Airflow variable 'source_names' and failing this DAG.")

        new_prarms = PARAMS
        new_prarms["source_names"] = source_names
        Variable.set(DAG_ID, new_prarms, serialize_json=True)
        variable_path = os.path.join(envs.PROJECT_ROOT, "src/airflow_dags/variables/variables.json")
        with open(variable_path, 'r') as f:
            data = json.load(f)

        data[DAG_ID] = new_prarms

        with open(variable_path, 'w') as f:
            json.dump(data, f, indent=2)
        logger.error("Airflow variable 'source_name' has been updated for this DAG.")

        raise Exception("Rerunning the DAG will fix issue.")


start = PythonOperator(
    task_id='start_task',
    python_callable=start_up,
    dag=dag)

complete = DummyOperator(
    task_id='All_jobs_completed',
    dag=dag)

for source in SOURCE_NAMES[:1]:
    start >> create_extract_task(source) >> file_mover(source) >> update_wm(source) >> complete
