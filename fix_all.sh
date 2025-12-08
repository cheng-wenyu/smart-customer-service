#!/bin/bash
echo "🚀 开始修复Docker部署问题..."

# 1. 停止所有服务
docker compose down

# 2. 基于requirements_alt.txt创建完整的requirements.txt
echo "📦 生成完整的requirements.txt..."
cat > requirements.txt << 'REQ_EOF'
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
requests==2.31.0
chromadb==0.4.15
transformers==4.35.0
numpy==1.24.3
torch==2.0.1
prometheus-client==0.19.0
psutil==5.9.6
sentencepiece==0.1.99
protobuf==4.25.1
REQ_EOF

echo "✅ 生成的requirements.txt内容："
cat requirements.txt

# 3. 检查代码是否需要修改
echo "🔍 检查代码中的导入语句..."
if grep -q "sentence_transformers" src/api_service_mlops_fixed.py; then
    echo "⚠️  检测到sentence_transformers导入，可能需要修改为transformers"
    echo "   如果代码报错，可能需要调整导入方式"
else
    echo "✅ 代码中没有sentence_transformers导入"
fi

# 4. 重新构建
echo "🔨 重新构建Docker镜像..."
docker compose build --no-cache

# 5. 启动服务
echo "⚡ 启动服务..."
docker compose up -d

# 6. 等待服务启动
echo "⏳ 等待服务启动（60秒）..."
sleep 60

# 7. 检查状态
echo "📊 检查服务状态..."
docker compose ps

echo ""
echo "🎯 测试连接："
echo "健康检查：curl http://localhost:8000/health"
echo "监控指标：curl http://localhost:8000/metrics"
echo "Prometheus：http://localhost:9090"
echo "Grafana：http://localhost:3000 (admin/admin123)"
