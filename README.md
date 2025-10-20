### 로컬에서 Edge Worker 실행해서 도커 컨테이너의 메인 웹서버와 통신
```shell
# 가상환경에서 AIRFLOW_HOME 설정
export AIRFLOW_HOME=$(pwd)

# 커멘드 실행 시, airflow.providers.edge3.executors.EdgeExecutor를 리턴해야 함.
airflow config get-value core executor

# 실행
airflow edge worker
```