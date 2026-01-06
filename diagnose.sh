#!/bin/bash
echo "=== Docker 服务诊断 ==="
echo "1. 容器状态:"
docker-compose ps

echo -e "\n2. Web 服务日志（最后20行）:"
docker-compose logs --tail=20 web

echo -e "\n3. 端口检查:"
if docker-compose ps | grep -q "Up"; then
    echo "✅ 容器正在运行"
    # 尝试从容器内部访问
    CONTAINER_ID=$(docker-compose ps -q web)
    if [ -n "$CONTAINER_ID" ]; then
        echo "尝试从容器内部访问服务..."
        docker exec $CONTAINER_ID curl -s http://localhost:5000/health 2>/dev/null || \
        docker exec $CONTAINER_ID curl -s http://localhost:5000 2>/dev/null || \
        echo "容器内部也无法访问"
    fi
else
    echo "❌ 容器没有运行"
fi

echo -e "\n4. 本地端口测试:"
curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/health 2>/dev/null || echo "无法连接"
echo " (HTTP 状态码)"

echo -e "\n5. 查看服务配置:"
grep -A5 -B5 "5000" docker-compose.yml 2>/dev/null || echo "未找到 docker-compose.yml"
