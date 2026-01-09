#!/bin/bash
echo "=== 环境诊断报告 ==="
echo "时间: $(date)"
echo ""

echo "1. Conda环境状态:"
echo "   当前环境: $(conda info --envs | grep '*' | awk '{print $1}')"
echo "   Python版本: $(python --version)"
echo "   Python路径: $(which python)"
echo ""

echo "2. 关键包版本:"
python -c "
try:
    import fastapi, uvicorn
    print(f'   FastAPI: {fastapi.__version__}')
    print(f'   Uvicorn: {uvicorn.__version__}')
except ImportError as e:
    print(f'   ❌ 缺少包: {e}')
"
echo ""

echo "3. 检查项目文件:"
if [ -f "src/api_service_final.py" ]; then
    echo "   ✅ src/api_service_final.py 存在"
    echo "   前3行:"
    head -3 src/api_service_final.py
else
    echo "   ❌ src/api_service_final.py 不存在"
fi
echo ""

echo "4. 测试导入应用:"
python -c "
import sys
sys.path.insert(0, '.')
try:
    from src.api_service_final import app
    print('   ✅ 应用导入成功')
    
    # 检查路由
    if hasattr(app, 'router'):
        routes = [route.path for route in app.router.routes[:5]]
        print(f'   前5个路由: {routes}')
    else:
        print('   ⚠️ 应用没有router属性')
        
except Exception as e:
    print(f'   ❌ 导入失败: {e}')
    import traceback
    traceback.print_exc()
"
echo ""

echo "5. 端口占用检查:"
if command -v lsof &> /dev/null; then
    lsof -i:8000 2>/dev/null || echo "   端口8000未被占用"
else
    echo "   使用netstat检查端口..."
    netstat -tlnp 2>/dev/null | grep :8000 || echo "   端口8000未被占用"
fi
