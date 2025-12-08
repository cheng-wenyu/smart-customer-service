#!/bin/bash
echo "🚀 启动智能客服系统（MLOps监控修复版）..."

# 检查必要的包
echo "📦 检查依赖包..."
pip list | grep -E "(prometheus-client|psutil|fastapi|uvicorn)" || {
    echo "安装缺失的依赖..."
    pip install prometheus_client psutil fastapi uvicorn > /dev/null 2>&1
}

echo "🌐 启动主API服务（端口8000）..."
echo "📊 指标服务器会自动启动在端口8001"
echo ""

# 直接运行修复版的服务
python src/api_service_mlops_fixed.py
