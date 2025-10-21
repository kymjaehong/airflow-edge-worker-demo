## README.md
* 배경
    * 매일 외부 서비스로부터 파일을 다운로드 -> 파싱 -> DB 적재를 하는 일련의 케이스가 있다고 가정
    * 팀 내에 할당 받은 NAS에 다양한 파일들을 저장 및 관리
* 유스케이스
    * 파일을 가져와 저장하는 Task와 파싱하고 적재하는 Task를 다른 서버에서 동작하게 해야 함.
        * 파싱하고 적재하는 Task는 정말 다양하기 때문에 메인 서버에서 동작.
        * 파일을 가져와 저장하는 Task는 이에 비해 현저히 적음.
    * Airflow 3.0에서 EdgeExecutor 기능이 추가됐는데 HTTPS|HTTP 통신을 통해 DAG를 공유하고 Task를 별도의 서버에서 동작시킬 수 있음.

## Multiple Executors (Celery + Edge)

Airflow의 Multiple Executors 기능을 사용하여, 메인 서버(`CeleryExecutor`)와 별도의 서버(`EdgeExecutor`)로 구성된 ETL 파이프라인 데모입니다.

주요 목적은 별도의 서버에서 **공용 NAS**에 일일 파일을 생성(Produce)하고, 이 이벤트를 감지한 메인 서버가 해당 파일을 읽어(Consume) 데이터를 처리하는 것입니다.

## 공식 Docs 참고

이 프로젝트의 아키텍처는 [Airflow Edge Executor 공식 문서](https://airflow.apache.org/docs/apache-airflow-providers-edge3/stable/architecture.html)을 참고했습니다.


```
                    [ 메인 서버 ]                                [ 별도 서버 (Edge worker) ]
      +-------------------------------------------+         +----------------------------+
      |  [ Webserver (UI + API) ]                 |         |                            |
      |    - AIRFLOW__EDGE__API_ENABLED=true      |         |                            |
      |                                           |         |  [ Airflow Edge Worker ]   |
      |  [ Scheduler ]                            |         |    - (name: 8bff...)       |
      |  [ DAG Processor ]                        |         |    - --queue edge_queue    |
      |                                           |         |                            |
      |  [ Celery Workers ]                       |         |                            |
      |    - (메인 서버)                            |         |                            |
      |                                           |         |                            |
      |  [ DB (MySQL) ]  [ Broker (Redis) ]       |         |                            |
      +-------------------------------------------+         +----------------------------+
               |        ^         |                                  |
(4. 작업 요청).  |        | (7. task 결과 전송)                           | (6. NAS에 파일 쓰기)
               |        |         |                                  |
               |        +---------+----------------------------------+
               v
      +--------------------------------------------------------------------------+
      |                           [ 공용 NAS (Shared Volume) ]                    |
      |                           - ./filestorage                                |
      +--------------------------------------------------------------------------+
               |
(8. 파일 읽기)   |
               +
```

### 데이터 흐름 (파이프라인)

1.  메인 서버에서 `producer_dag`가 실행됩니다.
2.  이 DAG의 `task_for_celery_worker`는 메인 서버의 **Celery 워커**에서 실행됩니다.
3.  `task_for_edge_worker`는 `executor="EdgeExecutor"` 및 `queue="edge_queue"`로 지정되어 있습니다.
4.  메인 서버 (Scheduler)는 이 작업을 별도 서버 (Edge Worker `8bff...`)에게 HTTP 통신을 통해 보냅니다.
5.  별도 서버 (Edge Worker)는 작업을 받아 `task_for_edge_worker` 함수를 실행합니다.
6.  별도 서버는 공용 NAS(`../filestorage`)에 `20251020.txt` 같은 파일을 저장합니다.
7.  작업이 성공하면, 별도 서버는 `Asset`(`nas_filestorage`)이 업데이트되었다는 이벤트를 발생시킵니다.
8.  메인 서버 (Scheduler)는 `Asset`(`nas_filestorage`)이 갱신된 것을 감지하고, `consumer_dag`를 자동으로 트리거합니다.
9. `consumer_dag`의 `process_file_from_nas` 태스크는 메인 서버 (Celery 워커)에서 실행되어, 공용 NAS에서 `20251020.txt` 파일을 읽어 데이터를 처리합니다.

### 로컬에서 Edge Worker를 실행해서 도커 컨테이너의 메인 웹서버와 통신한다면,
```shell
# 가상환경에서 AIRFLOW_HOME 설정
export AIRFLOW_HOME=$(pwd)

# 커멘드 실행 시, airflow.providers.edge3.executors.EdgeExecutor를 리턴해야 함.
airflow config get-value core executor

# 실행
airflow edge worker  --queue edge_queue
```