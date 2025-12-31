#!/bin/bash
cd /home/smart-customer-service

# 停止可能已经在运行的8001端口服务
fuser -k 8001/tcp 2>/dev/null

# 检查是否在虚拟环境中，如果不是则创建
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install flask requests -q

# 启动AI代理服务
echo "启动AI代理服务在端口 8001..."
nohup python ai_proxy.py > ai_proxy.log 2>&1 &

# 等待服务启动
sleep 3

# 测试服务
echo "测试服务..."
curl -s http://localhost:8001/health
echo ""
echo "✅ AI代理服务已启动"
echo "📝 日志文件: /home/smart-customer-service/ai_proxy.log"
echo "🌐 测试接口: curl -X POST http://localhost:8001/api/chat -H 'Content-Type: application/json' -d '{\"question\":\"你好\"}'"
