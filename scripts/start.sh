#!/usr/bin/env bash

set -e

cd "$(dirname "$0")/.."

echo "================================"
echo "          FJAI V1"
echo "================================"
echo

# 检查虚拟环境
if [ ! -f ".venv/bin/python" ]; then
    echo "[ERROR] 找不到 Python 虚拟环境"
    echo
    echo "请先运行："
    echo "  ./scripts/setup.sh"
    exit 1
fi

# 激活虚拟环境
source ".venv/bin/activate"

echo "[INFO] Python:"
python --version
echo

echo "[INFO] 启动 FJAI..."
echo

python -m backend.main