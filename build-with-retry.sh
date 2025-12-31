#!/bin/bash
echo "🔨 带重试的Docker构建脚本"
echo "========================="

MAX_RETRIES=3
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    echo "尝试构建 (第 $((RETRY_COUNT+1)) 次)..."
    
    # 尝试构建
    if docker-compose build --no-cache --progress=plain; then
        echo "✅ 构建成功！"
        exit 0
    else
        RETRY_COUNT=$((RETRY_COUNT+1))
        echo "❌ 构建失败，等待10秒后重试..."
        sleep 10
        
        # 如果是第一次失败，尝试更换镜像源
        if [ $RETRY_COUNT -eq 1 ]; then
            echo "尝试更换为更快的镜像源..."
            sed -i '1s/.*/FROM python:3.9-alpine/' Dockerfile
        fi
    fi
done

echo "❌ 构建失败，已达到最大重试次数"
echo "💡 建议："
echo "1. 检查网络连接"
echo "2. 手动拉取基础镜像: docker pull python:3.9-slim"
echo "3. 使用更小的镜像: python:3.9-alpine"
exit 1
