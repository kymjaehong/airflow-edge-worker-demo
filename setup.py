from setuptools import setup, find_packages

setup(
    name="myapp",
    version="0.1.0",
    packages=find_packages(
        exclude=['base', 'filestorage', 'logs', 'dags'],
    ),
)

# python setup.py install
# editable mode (개발 모드)가 아니라서, 수정할 때마다 다시 커멘드를 호출해야 함.

# pip install -e . 
# setuptools와 wheel을 이용해서 패키지를 개발용으로 링크만 걸어줌.
# pip install setuptools wheel (필요한 모듈)

# 요즘은 pytoml을 이용해서 관리함.
