#!/usr/bin/env python
"""
RAG项目启动脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """启动RAG服务"""
    print("=== 智能客服RAG系统 ===")
    print("请选择要启动的服务版本：")
    print("1. 基础版本 (api_service_fixed.py)")
    print("2. LangChain版本 (api_service_langchain_fixed.py)")
    print("3. MLOps监控版本 (api_service_mlops_fixed.py)")
    print("4. 最终监控版本 (api_service_final_monitored.py)")
    
    choice = input("\n请选择 (1-4): ").strip()
    
    service_files = {
        '1': 'src/api_service_fixed.py',
        '2': 'src/api_service_langchain_fixed.py',
        '3': 'src/api_service_mlops_fixed.py',
        '4': 'src/api_service_final_monitored.py'
    }
    
    if choice in service_files:
        file_path = service_files[choice]
        print(f"\n正在启动: {file_path}")
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            print(f"错误: 文件 {file_path} 不存在!")
            return
        
        # 尝试导入并运行
        try:
            # 动态导入
            import importlib.util
            spec = importlib.util.spec_from_file_location("service_module", file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            print("服务启动成功!")
            print("请访问: http://localhost:8000")
            print("按 Ctrl+C 停止服务")
            
        except Exception as e:
            print(f"启动失败: {e}")
            print("\n尝试直接运行文件...")
            os.system(f"python {file_path}")
    else:
        print("无效的选择!")

if __name__ == "__main__":
    main()
