FROM apache/airflow:3.1.0-python3.12

# 컨테이너 안에서 명령어를 실행할 사용자 지정
# 보안을 위해 ROOT 사용자 X
USER airflow
# 이미지를 만들 때 함께 실행할 명령어
RUN pip install --no-cache-dir pymysql apache-airflow-providers-edge3 apache-airflow-providers-celery