#!/bin/bash
echo "=== 验证依赖安装结果 ==="
echo "当前环境: $(conda env list | grep '*' | awk '{print $1}')"
echo ""

# 检查关键包
echo "1. 检查关键包版本:"
python -c "
packages = {
    'fastapi': 'fastapi',
    'uvicorn': 'uvicorn',
    'chromadb': 'chromadb',
    'sentence-transformers': 'sentence_transformers',
    'langchain': 'langchain',
    'pydantic': 'pydantic'
}

for display_name, import_name in packages.items():
    try:
        exec(f'import {import_name}')
        version = eval(f'{import_name}.__version__')
        print(f'   ✅ {display_name}: {version}')
    except ImportError:
        print(f'   ❌ {display_name}: 未安装')
    except AttributeError:
        print(f'   ✅ {display_name}: 已安装（无版本信息）')
"

echo ""
echo "2. 测试项目导入:"
python -c "
import sys
try:
    # 确保src目录在路径中
    sys.path.insert(0, '.')
    
    # 尝试导入应用
    from src.api_service_final import app
    print('   ✅ 应用导入成功')
    
    # 检查路由
    routes = [route.path for route in app.router.routes[:5]]
    print(f'   前5个路由: {routes}')
    
except ImportError as e:
    print(f'   ❌ 导入失败: {e}')
    print('   可能缺少某些依赖')
except Exception as e:
    print(f'   ❌ 其他错误: {e}')
"

echo ""
echo "3. 查看安装的包总数:"
pip list | wc -l | awk '{print "   已安装包数量:", $1-2}'
