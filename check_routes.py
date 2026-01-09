import sys
sys.path.insert(0, '.')
try:
    from src.api_service_final import app
    print('✅ [干净容器内] FastAPI应用导入成功！')
    routes = [route.path for route in app.routes if hasattr(route, 'path')]
    print(f'✅ [干净容器内] 定义的路由: {routes}')
    if '/ask' in routes:
        print('🎯 关键确认: POST /ask 路由已存在于代码中！')
    else:
        print('⚠️  注意: /ask 路由未在代码中找到，需要检查路由定义。')
except Exception as e:
    print(f'❌ 导入失败: {e}')
    import traceback
    traceback.print_exc()
