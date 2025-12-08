#!/bin/bash
echo "🧪 测试MLOps监控系统..."

echo "1. 测试健康检查："
curl -s http://localhost:8000/health | python -m json.tool

echo ""
echo "2. 测试系统状态："
curl -s http://localhost:8000/system/status | python -m json.tool

echo ""
echo "3. 查看监控指标："
curl -s http://localhost:8001 | head -20

echo ""
echo "4. 测试问答功能："
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "退货需要什么条件", "top_k": 3}' \
  -s | python -m json.tool

echo ""
echo "✅ 测试完成！"
