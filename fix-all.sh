#!/bin/bash
echo "🔧 完整修复部署问题"
echo "======================"

SERVER="121.43.254.207"

echo "1. 上传所有必要文件到服务器..."
cd ~/smart-customer-service

# 创建要上传的文件列表
FILES_TO_UPLOAD=(
    "Dockerfile"
    "Dockerfile.app"
    "Dockerfile.base"
    "config.py"
    "prometheus.yml"
    "*.py"
)

# 上传文件
for pattern in "${FILES_TO_UPLOAD[@]}"; do
    for file in $pattern; do
        if [ -f "$file" ]; then
            echo "  上传: $file"
            scp "$file" root@$SERVER:/home/smart-customer-service/
        fi
    done
done

# 上传目录
DIRS_TO_UPLOAD=("src" "prometheus" "static" "templates")
for dir in "${DIRS_TO_UPLOAD[@]}"; do
    if [ -d "$dir" ]; then
        echo "  上传目录: $dir/"
        scp -r "$dir" root@$SERVER:/home/smart-customer-service/
    fi
done

echo ""
echo "2. 在服务器上修正配置..."
ssh root@$SERVER << 'REMOTE_EOF'
cd /home/smart-customer-service

echo "当前目录: $(pwd)"
echo "文件列表:"
ls -la

echo ""
echo "检查docker-compose.yml..."
if [ -f "docker-compose.yml" ]; then
    echo "服务名列表:"
    grep -E '^[[:space:]]*[a-zA-Z][a-zA-Z0-9_-]*:' docker-compose.yml
    
    # 创建修正的deploy.sh
    echo "创建新的deploy.sh..."
    cat > deploy.sh << 'DEPLOYEOF'
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
DEPLOYEOF

    chmod +x deploy.sh
    echo "✅ 配置修正完成"
else
    echo "❌ docker-compose.yml 不存在"
fi
REMOTE_EOF

echo ""
echo "3. 运行测试部署..."
ssh root@$SERVER "cd /home/smart-customer-service && ./deploy.sh"

echo ""
echo "✅ 修复完成！"
echo "访问地址: http://121.43.254.207:5000"
