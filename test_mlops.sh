#!/bin/bash
echo "🧪 测试MLOps监控系统..."

# 等待服务启动
sleep 2

echo ""
echo "1. 测试健康检查："
curl -s http://localhost:8000/health | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(f'状态: {data[\"status\"]}')
    print(f'CPU使用率: {data[\"system\"][\"cpu_percent\"]}%')
    print(f'内存使用率: {data[\"system\"][\"memory_percent\"]}%')
except:
    print('服务可能未启动')
"

echo ""
echo "2. 测试系统状态："
curl -s http://localhost:8000/system/status | python3 -m json.tool 2>/dev/null || echo "服务可能未启动"

echo ""
echo "3. 查看监控指标："
curl -s http://localhost:8000/metrics 2>/dev/null | grep -E "(http_requests_total|rag_queries_total|system_cpu)" | head -5 || echo "指标端点可能未就绪"

echo ""
echo "4. 测试问答功能："
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "退货需要什么条件", "top_k": 3}' \
  -s 2>/dev/null | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(f'问题: {data[\"question\"]}')
    print(f'回答: {data[\"answer\"][:50]}...')
    print(f'处理时间: {data[\"processing_time\"]}秒')
except:
    print('问答服务可能未就绪')
"

echo ""
echo "✅ 测试完成！"
echo "📊 可以在浏览器中访问: http://localhost:8000/docs"
