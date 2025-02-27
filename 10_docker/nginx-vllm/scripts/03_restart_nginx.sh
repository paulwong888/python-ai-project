#!/bin/bash

# 获取当前脚本的路径
SCRIPT_PATH="$(realpath "$0")"
echo "当前脚本的路径是: $SCRIPT_PATH"

# 获取当前脚本所在的目录
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"
echo "当前脚本所在的目录是: $SCRIPT_DIR"
cd $SCRIPT_DIR

source ./00_varible.sh

# docker compose stop nginx-webui
# docker compose start nginx-webui
SERVICE_NAME=nginx-vllm

docker compose down ${SERVICE_NAME}
docker compose up -d ${SERVICE_NAME}
docker compose logs -f ${SERVICE_NAME}
# echo ${DOCKER_ROOT_DIR}