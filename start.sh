#!/bin/bash

echo "🚀 Smart Customer Service 启动脚本"
echo "=================================="

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker：https://docs.docker.com/get-docker/"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "安装Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# 创建必要的目录
echo "创建必要的目录..."
mkdir -p logs chroma_db/data triton_models prometheus_data grafana_data

# 设置权限
chmod -R 755 logs
chmod -R 755 chroma_db

# 构建并启动服务
echo "构建并启动Docker服务..."
docker-compose down 2>/dev/null
docker-compose build --no-cache
docker-compose up -d

echo ""
echo "✅ 启动完成！"
echo ""
echo "📊 服务状态："
echo "  前端界面: http://localhost:5000"
echo "  Triton推理服务: http://localhost:8000"
echo "  Chroma向量数据库: http://localhost:8003"
echo "  Prometheus监控: http://localhost:9090"
echo "  Grafana仪表板: http://localhost:3000"
echo ""
echo "🔧 常用命令："
echo "  查看所有日志: docker-compose logs -f"
echo "  查看Web服务日志: docker-compose logs -f web"
echo "  停止服务: docker-compose down"
echo "  重启服务: docker-compose restart"
echo ""
echo "📝 健康检查："
echo "  运行: curl http://localhost:5000/health"
echo ""
