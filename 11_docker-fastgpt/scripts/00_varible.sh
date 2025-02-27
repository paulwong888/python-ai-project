#!/bin/bash

# 获取当前脚本的路径
# SCRIPT_PATH="$(realpath "$0")"
# echo "当前脚本的路径是: $SCRIPT_PATH"

# 获取当前脚本所在的目录
# SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"
# echo "当前脚本所在的目录是: $SCRIPT_DIR"
# cd $SCRIPT_DIR

# export HTTP_PROXY=http://192.168.0.102:7890
# export HTTPS_PROXY=https://192.168.0.102:7890


export DOCKER_ROOT_DIR=/home/paul/paulwong/work/workspaces/python-ai-project/docker-fastgpt/data
export NGINX_DATA_DIR=${DOCKER_ROOT_DIR}/nginx