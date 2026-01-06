#!/bin/bash

echo "📦 开始部署 Smart Customer Service..."
echo "======================================="

# 停止并删除旧容器
echo "清理旧容器..."
docker-compose down 2>/dev/null

# 拉取最新的代码
echo "更新代码..."
git pull origin main

# 检查是否要安装Triton（如果有GPU）
if command -v nvidia-smi &> /dev/null; then
    echo "🎮 检测到NVIDIA GPU，准备安装Triton推理服务..."
    if ! docker images | grep -q "tritonserver"; then
        echo "下载Triton镜像..."
        docker pull nvcr.io/nvidia/tritonserver:23.10-py3
    fi
    # 创建Triton模型目录（如果不存在）
    mkdir -p triton_models
    echo "✅ GPU加速模式已启用"
else
    echo "💻 未检测到GPU，使用CPU模式运行"
fi

# 检查Docker镜像是否存在，不存在则构建
echo "检查并构建Docker镜像..."
docker-compose build --no-cache

# 启动所有服务
echo "启动所有服务..."
docker-compose up -d

# 等待服务启动
echo "等待服务启动..."
sleep 10

# 检查服务状态
echo "📊 服务状态检查："
services=("web" "chromadb" "prometheus" "grafana")
for service in "${services[@]}"; do
    if docker-compose ps | grep -q "$service.*Up"; then
        echo "  ✅ $service 运行正常"
    else
        echo "  ❌ $service 启动失败"
    fi
done

# 显示访问信息
SERVER_IP=$(hostname -I | awk '{print $1}')
echo ""
echo "🎉 部署完成！"
echo ""
echo "🌐 访问地址："
echo "  本地访问：http://localhost:5000"
echo "  网络访问：http://$SERVER_IP:5000"
echo ""
echo "📈 监控面板："
echo "  Grafana: http://$SERVER_IP:3000 (admin/admin)"
echo "  Prometheus: http://$SERVER_IP:9090"
echo ""
echo "🔍 查看日志："
echo "  docker-compose logs -f web"
echo ""
