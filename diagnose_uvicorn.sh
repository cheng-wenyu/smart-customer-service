#!/bin/bash

echo "=== Uvicorn进程诊断 ==="
echo ""

echo "1. 查看容器状态："
docker-compose -f docker-compose.dev.yml ps rag-service

echo -e "\n2. 查看容器内所有进程："
docker exec smart-customer-service_rag-service_1 ps aux

echo -e "\n3. 查看容器启动命令："
docker inspect smart-customer-service_rag-service_1 | grep -A2 -B2 '"Cmd"\|"Command"\|"Entrypoint"'

echo -e "\n4. 查看容器日志："
docker-compose -f docker-compose.dev.yml logs --tail=20 rag-service

echo -e "\n5. 测试run.py是否能导入："
docker exec smart-customer-service_rag-service_1 python -c "
try:
    import run
    print('✅ run.py可以导入')
    if hasattr(run, 'app'):
        print('✅ app实例存在')
        from fastapi import FastAPI
        if isinstance(run.app, FastAPI):
            print('✅ app是FastAPI实例')
        else:
            print('❌ app不是FastAPI实例:', type(run.app))
    else:
        print('❌ run.py中没有app实例')
        print('  找到的属性:', [attr for attr in dir(run) if not attr.startswith('_')])
except Exception as e:
    print('❌ 导入失败:', e)
"

echo -e "\n6. 尝试手动启动uvicorn："
docker exec smart-customer-service_rag-service_1 bash -c "cd /app && python -m uvicorn run:app --host 0.0.0.0 --port 8000 --reload &"
sleep 2
echo "查看进程："
docker exec smart-customer-service_rag-service_1 ps aux | grep uvicorn
