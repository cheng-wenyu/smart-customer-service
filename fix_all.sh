#!/bin/bash
echo "=== 一键修复脚本 ==="

# 1. 安装依赖
echo "安装python3-venv..."
sudo apt update && sudo apt install python3.12-venv python3-pip -y

# 2. 停止旧服务
echo "停止旧服务..."
sudo fuser -k 8001/tcp 2>/dev/null

# 3. 安装Flask
echo "安装Flask..."
pip3 install --break-system-packages flask requests

# 4. 启动AI服务
echo "启动AI服务..."
cd /home/smart-customer-service
nohup python3 simple_ai_proxy.py > simple_ai_proxy.log 2>&1 &

# 5. 更新Nginx配置
echo "更新Nginx配置..."
CONTAINER_ID=$(docker ps --filter "ancestor=nginx" --format "{{.ID}}" | head -1)
if [ -z "$CONTAINER_ID" ]; then
    CONTAINER_ID=$(docker ps --format "{{.ID}} {{.Names}}" | grep -E "web|nginx" | head -1 | awk '{print $1}')
fi

cat > /tmp/nginx.conf << 'NGINXCONF'
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api/chat {
        proxy_pass http://host.docker.internal:8001/api/chat;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
NGINXCONF

docker cp /tmp/nginx.conf $CONTAINER_ID:/etc/nginx/conf.d/default.conf
docker exec $CONTAINER_ID nginx -s reload

# 6. 测试
echo "等待服务启动..."
sleep 3

echo -e "\n=== 测试结果 ==="
echo "AI服务健康检查:"
curl -s http://localhost:8001/health || echo "AI服务未启动"

echo -e "\nWeb服务测试:"
curl -s -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question":"测试"}' | grep -o '"answer":"[^"]*"' | head -1

echo -e "\n✅ 完成！"
echo "Web界面: http://121.43.254.207:5000"
echo "AI服务日志: tail -f /home/smart-customer-service/simple_ai_proxy.log"
