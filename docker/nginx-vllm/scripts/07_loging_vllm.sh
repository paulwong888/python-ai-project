#!/bin/bash

# 获取当前脚本的路径
SCRIPT_PATH="$(realpath "$0")"
echo "当前脚本的路径是: $SCRIPT_PATH"

# 获取当前脚本所在的目录
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"
echo "当前脚本所在的目录是: $SCRIPT_DIR"
cd $SCRIPT_DIR

source ./00_varible.sh

SERVICE_NAME=vllm

docker compose exec ${SERVICE_NAME} /bin/bash
# echo ${DOCKER_ROOT_DIR}