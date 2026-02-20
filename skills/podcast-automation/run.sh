#!/bin/bash
# 本地运行播客生成器

cd "$(dirname "$0")"

# 检查 .env
if [ ! -f ".env" ]; then
    echo "❌ 错误: .env 文件不存在"
    echo "   请复制 .env.example 为 .env 并填写配置"
    exit 1
fi

# 加载环境变量
export $(grep -v '^#' .env | xargs)

# 运行
python3 scripts/generate-podcast.py
