# explore_project.py - 探索项目结构
import importlib
import sys
import os

sys.path.append('src')

# 尝试导入可能存在的模块
modules_to_try = [
    'api_service',
    'api_service_final',
    'api_service_final_monitored',
    'api_service_fixed',
    'api_service_mlops_fixed',
    'vector_search',
    'llm_generator'
]

for module_name in modules_to_try:
    try:
        module = importlib.import_module(module_name)
        print(f"\n✅ 成功导入: {module_name}")
        print(f"   文件: {module.__file__}")
        
        # 列出模块中的函数
        functions = [f for f in dir(module) if not f.startswith('_')]
        print(f"   函数列表: {functions[:10]}...")
        
        # 检查是否有查询处理函数
        query_funcs = [f for f in functions if 'query' in f.lower() or 
                      'process' in f.lower() or 
                      'answer' in f.lower() or
                      'rag' in f.lower()]
        if query_funcs:
            print(f"   可能的查询函数: {query_funcs}")
            
    except ImportError as e:
        print(f"❌ 无法导入 {module_name}: {e}")
