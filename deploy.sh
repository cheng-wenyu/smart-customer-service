#!/bin/bash

echo "📦 开始部署 Smart Customer Service..."
echo "======================================="

# 停止并删除旧容器
echo "清理旧容器..."
docker-compose down 2>/dev/null

# 检查是否要安装Triton（如果有GPU）
if command -v nvidia-smi &> /dev/null; then
    echo "🎮 检测到NVIDIA GPU，准备安装Triton推理服务..."
    if ! docker images | grep -q "tritonserver"; then
        echo "下载Triton镜像..."
        docker pull nvcr.io/nvidia/tritonserver:23.10-py3
    fi
    mkdir -p triton_models
    echo "✅ GPU加速模式已启用"
else
    echo "💻 未检测到GPU，使用CPU模式运行"
fi

# 构建镜像
echo "构建Docker镜像..."
docker-compose build --no-cache

# 启动服务
echo "启动所有服务..."
docker-compose up -d

# 等待并检查状态
echo "等待服务启动..."
sleep 15

echo "📊 服务状态："
docker-compose ps

# 显示访问信息
SERVER_IP=$(hostname -I | awk '{print \$1}')
echo ""
echo "🎉 部署完成！"
echo ""
echo "🌐 访问地址："
echo "  Web应用: http://\$SERVER_IP:5000"
echo "  Grafana监控: http://\$SERVER_IP:3000 (admin/admin)"
echo "  Prometheus: http://\$SERVER_IP:9090"
echo ""
echo "🔧 常用命令："
echo "  查看日志: docker-compose logs -f"
echo "  停止服务: docker-compose down"
echo "  重启服务: docker-compose restart"
