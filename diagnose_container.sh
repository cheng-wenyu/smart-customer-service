#!/bin/bash
echo "🔍 Docker容器诊断工具"
echo "====================="

# 检查容器状态
echo "1. 容器状态:"
docker-compose ps

echo -e "\n2. 容器内进程:"
docker-compose exec rag-service ps aux

echo -e "\n3. 检查模型文件:"
docker-compose exec rag-service ls -la /app/data/models/

echo -e "\n4. 检查Python包:"
docker-compose exec rag-service python -c "
import sys
print('Python版本:', sys.version)
print('Python路径:')
for p in sys.path:
    print(' ', p)
"

echo -e "\n5. 尝试启动正确的应用:"
docker-compose exec rag-service python -c "
try:
    from src.api_service_final import app
    print('✅ 可以导入app')
    
    # 检查是否有FastAPI应用的方法
    if hasattr(app, 'routes'):
        print('✅ app有routes属性')
        print(f'   路由数量: {len(app.routes)}')
        for route in app.routes[:3]:
            print(f'   - {route.path if hasattr(route, \"path\") else route}')
    
except Exception as e:
    print('❌ 导入失败:')
    import traceback
    traceback.print_exc()
"

echo -e "\n6. 查看错误日志:"
docker-compose logs --tail=20 rag-service
