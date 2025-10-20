import pendulum

from airflow.sdk import dag, task
from assets import my_file_asset

@dag(
    "consumer_dag",
    # timezone-aware한 pendulum
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    schedule=[my_file_asset],
    catchup=False,
    default_args={
        'owner': 'me',
        'description': 'EdgeExecutor가 파일을 NAS에 저장하면, DAG가 실행됩니다.',
    },
    tags=['main', 'consumer'],
)
def consumer_dag():
    @task
    def start():
        print("START CONSUMER!!!!!!")
        
    @task
    def process_file_from_nas():
        """
        NAS에 있는 파일을 읽어 작업을 진행합니다.
        """
        nas_path = "/opt/airflow/filestorage/"  # 절대 경로 사용

        from datetime import datetime
        str_now = datetime.now().strftime('%Y%m%d')

        import os
        files = os.listdir(nas_path)
        filtered = list(f for f in files if f.split('.')[0].startswith(str_now))
        if not filtered:
            print("================= NOT FOUND FILES =================")
            return "None"

        for file in filtered:
            try:
                with open(f"{nas_path}{file}", "r") as f:
                    content = f.read()
                    print("--- File Content ---")
                    print(content)
                    print("---------------------------------------------")
                    return content
            except FileNotFoundError:
                print(f"Error: File not found at {nas_path}{file}")
                raise

        return filtered
    
    start() >> process_file_from_nas()

consumer_dag()
