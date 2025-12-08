#!/bin/bash
cd "$(dirname "$0")"

echo "🚀 启动智能客服系统..."
echo "📁 当前目录: $(pwd)"

# 检查必要文件
if [ ! -f "data/return_policy.txt" ]; then
    echo "📝 创建示例数据文件..."
    mkdir -p data
    echo "示例数据" > data/return_policy.txt
fi

# 修复src目录的__init__.py（确保是包）
if [ ! -f "src/__init__.py" ]; then
    echo "📝 创建src/__init__.py..."
    touch src/__init__.py
fi

# 运行API服务
echo "🌐 启动Web服务..."
echo "访问: http://localhost:8000"
echo "文档: http://localhost:8000/docs"
echo "按 Ctrl+C 停止服务"
echo "----------------------------------------"

# 使用模块方式运行
python -m src.api_service
