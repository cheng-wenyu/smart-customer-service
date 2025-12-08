#!/bin/bash
# MLOps部署脚本

set -e  # 出错时退出

echo "🚀 开始部署智能客服系统..."

# 1. 构建Docker镜像
echo "📦 构建Docker镜像..."
docker build -t smart-customer-service:latest .

# 2. 停止并删除旧容器
echo "🔄 清理旧容器..."
docker-compose down || true

# 3. 启动新服务
echo "⚡ 启动服务..."
docker-compose up -d

# 4. 等待服务就绪
echo "⏳ 等待服务启动..."
sleep 10

# 5. 健康检查
echo "🔍 执行健康检查..."
curl -f http://localhost:8000/health || exit 1

echo "✅ 部署成功！"
echo "🌐 API地址: http://localhost:8000"
echo "📊 监控地址: http://localhost:9090"
echo "📈 仪表板: http://localhost:3000"
