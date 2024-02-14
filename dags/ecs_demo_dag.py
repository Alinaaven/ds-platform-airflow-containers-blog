import datetime, os, json

from airflow.decorators import dag, task
from airflow.models import Variable
from airflow.operators.python import get_current_context
from airflow.providers.amazon.aws.operators.ecs import EcsRunTaskOperator


DAG_NAME = "ecs_demo_dag"

dag_path = os.path.dirname(os.path.abspath(__file__))

dag_vars = (Variable.get(key='environment_variables_demo', default_var=dict(), deserialize_json=True))


default_args = {
    'owner': 'my_name',
    'depends_on_past': False,
    'start_date': datetime.datetime(2023, 1, 1)
}


@dag(default_args=default_args, schedule_interval=None, max_active_runs=1, catchup=False)

def run_demo_ecs():

    @task
    def get_input_data():
        dag_path = os.path.dirname(os.path.abspath(__file__))
        input_file_path = os.path.join(dag_path, 'inputs.json')
        with open(input_file_path, 'r') as file:
            data = json.load(file)
        return data['inputs']
    
    @task
    def run_ecs_task(arg):
        aws_task_definition = 'MY_AWS_TASK_DEFINITION'
        aws_ecr_image_name = 'MY_AWS_ECR_IMAGE'
        ecs_task  = EcsRunTaskOperator(
            task_id=f'run_docker_{list(arg.keys())[0]}',
            task_definition=aws_task_definition,
            cluster=dag_vars.get('aws_cluster'),
            launch_type='FARGATE',
            overrides={
                    'containerOverrides': [
                        {
                            'name': aws_ecr_image_name,
                            'environment': [
                                {'name': 'SUBJECT_ID', 'value': str(arg['subject_id'])},
                                {'name': 'SAMPLE_ID', 'value': str(arg['sample_id'])}
                            ],
                        },
                    ],
                },
            network_configuration={
                    "awsvpcConfiguration": {
                        "securityGroups": dag_vars.get('aws_security_groups'),
                        "subnets": dag_vars.get('aws_subnets'),
                    },
                },
                awslogs_group=f'/ecs/{aws_task_definition}',
                awslogs_stream_prefix=f'ecs/{aws_ecr_image_name}'
        )
        ecs_task.execute(context=get_current_context())
        
    
    input_data_extractions_instance=get_input_data()
    run_tasks = run_ecs_task.expand(arg=input_data_extractions_instance)


    input_data_extractions_instance >> run_tasks


etl_bip_checkmate_dl_dag_instance = run_demo_ecs()
