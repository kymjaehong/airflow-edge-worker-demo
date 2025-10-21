import subprocess
from pathlib import Path

result = subprocess.run(
    ['bash', f'{Path(__file__).parent.parent}/test.sh', 'A'],
    capture_output=True,  # 표준 출력(stdout)과 표준 에러(stderr)을 파이썬이 변수로 캡처해서 bytes로 리턴
    text=True,  # 출력 결과를 bytes -> str 처리
)

print(result.stdout)  # b'hello\n' -> 'hello\n'
print(result.stderr)  # b'' -> 에러 출력

if result.returncode != 0:
    # raise ~
    print("ERROR!!!!!")
