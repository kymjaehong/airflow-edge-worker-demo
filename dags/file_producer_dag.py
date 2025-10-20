import pendulum
from airflow.sdk import dag, task

from assets import my_file_asset

@dag(
    "producer_dag",
    # timezone-aware한 pendulum
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    # ✅ 권장: 데이터셋 기반 DAG은 수동 실행을 위해 None으로 설정하는 경우가 많습니다.
    schedule=None,
    catchup=False,
    default_args={
        'owner': 'me',
        'description': '오늘의 파일을 NAS에 저장하고 에셋을 업데이트합니다.',
    },
    tags=['edge', 'producer'],
)
def producer_dag():
    @task(
        executor="airflow.providers.edge3.executors.EdgeExecutor",
        queue="edge_queue",
        outlets=[my_file_asset],
    )
    def task_for_edge_worker():
        # B서버(Edge)에서 실행될 로직
        print("This runs on the Edge Worker!")
        # ... (NAS 파일 저장 로직) ...
        """
        Edge Worker에서 새로운 파일을 생성해서 NAS에 저장합니다.
        """
        nas_path = "/opt/airflow/filestorage/"  # 절대 경로 사용
        
        from datetime import datetime
        str_now = datetime.now().strftime('%Y%m%d')
        content = f"File created from Server B at {str_now}"
        filenpath = f"{nas_path}{str_now}.txt"
        with open(filenpath, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"Successfully wrote to {filenpath} from Edge Worker")
        return filenpath

    @task
    def task_for_celery_worker():
        # A서버(Celery)에서 실행될 로직
        print("This runs on the Celery Worker!")

    task_for_celery_worker() >> task_for_edge_worker()

producer_dag()
