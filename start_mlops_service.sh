#!/bin/bash
echo "🚀 启动智能客服系统（MLOps监控版）..."

# 安装依赖（如果还没有）
pip install prometheus_client psutil fastapi uvicorn requests chromadb sentence-transformers > /dev/null 2>&1

# 创建日志目录
mkdir -p logs

echo "📊 启动监控指标服务器（端口8001）..."
python -m prometheus_client --port=8001 &
PROMETHEUS_PID=$!

echo "🌐 启动主API服务（端口8000）..."
python src/api_service_final_monitored.py &
API_PID=$!

echo "✅ 服务启动成功！"
echo "📍 API服务: http://localhost:8000"
echo "📊 监控指标: http://localhost:8001"
echo "📚 API文档: http://localhost:8000/docs"

echo ""
echo "📋 可用的端点："
echo "  • /           - 服务首页"
echo "  • /health     - 健康检查"
echo "  • /metrics    - Prometheus指标"
echo "  • /system/status - 系统状态"
echo "  • /ask        - 智能问答"
echo "  • /docs       - 交互式API文档"

echo ""
echo "🛑 按 Ctrl+C 停止服务"

# 等待用户按Ctrl+C
trap "kill $API_PID $PROMETHEUS_PID; echo '🛑 服务已停止'" SIGINT
wait
