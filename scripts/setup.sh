#!/usr/bin/env bash

set -e

cd "$(dirname "$0")/.."

echo "================================"
echo "       FJAI V1 Linux Setup"
echo "================================"
echo

# 检查 Python
if ! command -v python3 >/dev/null 2>&1; then
    echo "[ERROR] 找不到 Python 3"
    echo "请先安装 Python 3.11+"
    exit 1
fi

echo "[OK] Python:"
python3 --version
echo

# 创建虚拟环境
if [ ! -d ".venv" ]; then
    echo "[INFO] 创建 Python 虚拟环境..."
    python3 -m venv .venv
else
    echo "[INFO] .venv 已存在，跳过创建"
fi

# 激活虚拟环境
source ".venv/bin/activate"

echo
echo "[INFO] 升级 pip..."
python -m pip install --upgrade pip

echo
echo "[INFO] 安装 FJAI 依赖..."
pip install -r requirements.txt

echo
echo "================================"
echo "       FJAI 安装完成"
echo "================================"
echo
echo "启动："
echo "  ./scripts/start.sh"
echo