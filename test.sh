#!/bin/bash
set -euo pipefail

# 인자 존재 확인
if [ $# -lt 1 ]; then
  echo "[ERROR] 인자가 필요합니다. (예: ./example.sh A)"
  exit 1
fi

ARG=$1

echo "[INFO] 입력된 인자: $ARG"

if [ "$ARG" == "A" ]; then
  echo "[INFO] A이므로 정상 처리합니다."
  exit 0
elif [ "$ARG" == "B" ]; then
  echo "[ERROR] B이므로 에러로 종료합니다."
  exit 1
else
  echo "[WARN] 인자가 A 또는 B가 아닙니다. 기본적으로 통과합니다."
  exit 1
fi
