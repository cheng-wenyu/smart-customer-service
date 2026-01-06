#!/bin/bash
echo "🚀 快速启动 Smart Customer Service"

# 检查Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装"
    exit 1
fi

# 创建必要目录
mkdir -p logs chroma_db/data prometheus_data grafana_data

# 检查是否有GPU
if command -v nvidia-smi &> /dev/null; then
    echo "✅ 检测到GPU，使用GPU模式"
else
    echo "⚠️  未检测到GPU，使用CPU模式"
fi

# 启动服务
echo "启动服务..."
docker-compose up -d

# 显示状态
echo ""
echo "📊 服务状态："
docker-compose ps

echo ""
echo "🌐 访问地址："
echo "  Web界面: http://localhost:5000"
echo "  监控面板: http://localhost:3000"
echo ""
echo "🔍 查看日志: docker-compose logs -f web"
