#!/bin/bash
echo "🚀 一键部署到阿里云（使用国内镜像）"
echo "======================================"

SERVER="121.43.254.207"

echo "1. 登录服务器配置Docker镜像加速..."
ssh root@$SERVER << 'CONFIG_EOF'
# 配置阿里云镜像加速
cat > /etc/docker/daemon.json << 'DOCKER_CONFIG'
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com", 
    "https://mirror.baidubce.com",
    "https://registry.cn-hangzhou.aliyuncs.com"
  ],
  "max-concurrent-downloads": 10,
  "max-concurrent-uploads": 10
}
DOCKER_CONFIG

systemctl daemon-reload
systemctl restart docker
sleep 3
echo "✅ Docker镜像加速已配置"
CONFIG_EOF

echo ""
echo "2. 在服务器上创建项目文件..."
ssh root@$SERVER << 'PROJECT_EOF'
cd /home/smart-customer-service

# 创建目录
mkdir -p static grafana_data prometheus_data logs chroma_db/data triton_models

# 创建docker-compose.yml（使用国内镜像）
cat > docker-compose.yml << 'COMPOSE_EOF'
version: '3.8'

services:
  web:
    image: registry.cn-hangzhou.aliyuncs.com/acs/nginx:latest
    ports:
      - "5000:80"
    volumes:
      - ./static:/usr/share/nginx/html
    restart: always
  
  grafana:
    image: registry.cn-hangzhou.aliyuncs.com/acs/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_INSTALL_PLUGINS=grafana-piechart-panel
    volumes:
      - ./grafana_data:/var/lib/grafana
    restart: always
  
  prometheus:
    image: registry.cn-hangzhou.aliyuncs.com/acs/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - ./prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    restart: always
  
  chromadb:
    image: chromadb/chroma:latest
    ports:
      - "8003:8000"
    volumes:
      - ./chroma_db/data:/chroma/chroma
    restart: always
COMPOSE_EOF

# 创建静态页面
cat > static/index.html << 'HTML_EOF'
<!DOCTYPE html>
<html>
<head><title>智能客服系统</title></head>
<body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
    <h1>🎉 智能客服系统部署成功！</h1>
    <p>服务器: 121.43.254.207</p>
    <p>状态: <span style="color: green; font-weight: bold;">运行正常</span></p>
    <div style="margin: 30px;">
        <a href="http://121.43.254.207:3000" style="display: inline-block; padding: 10px 20px; background: #4CAF50; color: white; text-decoration: none; border-radius: 5px; margin: 5px;">监控面板</a>
        <a href="http://121.43.254.207:9090" style="display: inline-block; padding: 10px 20px; background: #2196F3; color: white; text-decoration: none; border-radius: 5px; margin: 5px;">指标服务</a>
    </div>
    <p style="margin-top: 30px; color: #666;">下一步：上传你的AI代码到 /home/smart-customer-service/src/</p>
</body>
</html>
HTML_EOF

# 创建prometheus配置
cat > prometheus.yml << 'PROM_EOF'
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
  
  - job_name: 'web'
    static_configs:
      - targets: ['web:80']
PROM_EOF

echo "✅ 项目文件创建完成"
PROJECT_EOF

echo ""
echo "3. 启动服务..."
ssh root@$SERVER << 'START_EOF'
cd /home/smart-customer-service

echo "停止旧服务..."
docker-compose down 2>/dev/null || true

echo "拉取镜像..."
docker-compose pull --quiet

echo "启动服务..."
docker-compose up -d

echo "等待服务启动..."
sleep 10

echo "服务状态:"
docker-compose ps
START_EOF

echo ""
echo "4. 测试访问..."
echo "等待20秒让服务完全启动..."
sleep 20

echo "测试Web服务..."
if curl -s -o /dev/null -w "%{http_code}" http://$SERVER:5000 | grep -q "200\|301\|302"; then
    echo "✅ Web服务可访问: http://$SERVER:5000"
else
    echo "⚠️  Web服务可能还在启动中，稍后重试"
fi

echo ""
echo "✅ 部署完成！"
echo ""
echo "🌐 访问地址:"
echo "  主页面: http://$SERVER:5000"
echo "  监控面板: http://$SERVER:3000 (admin/admin)"
echo "  指标服务: http://$SERVER:9090"
echo ""
echo "💡 下一步：将你的AI代码上传到服务器"
echo "  上传命令: scp -r src/ root@$SERVER:/home/smart-customer-service/"
