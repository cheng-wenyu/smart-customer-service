#!/usr/bin/env python3
# find_rag_core.py - 查找RAG核心函数的脚本

import os
import re
import sys

def search_rag_functions(directory="."):
    """搜索RAG相关函数"""
    print("=" * 80)
    print("搜索RAG核心函数...")
    print("=" * 80)
    
    rag_patterns = [
        r"def.*query", 
        r"def.*answer",
        r"def.*rag",
        r"def.*chat",
        r"def.*ask",
        r"class.*RAG",
        r"class.*Pipeline",
        r"@app\.post.*query",
        r"@app\.get.*query"
    ]
    
    for root, dirs, files in os.walk(directory):
        # 跳过一些目录
        if any(skip in root for skip in ['__pycache__', '.git', 'venv', 'env']):
            continue
            
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                    # 检查是否包含RAG相关函数
                    found = False
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        for pattern in rag_patterns:
                            if re.search(pattern, line, re.IGNORECASE):
                                if not found:
                                    print(f"\n📁 文件: {filepath}")
                                    print("-" * 40)
                                    found = True
                                # 显示匹配行和接下来的2行
                                context = '\n'.join(lines[max(0, i-1):min(len(lines), i+3)])
                                print(f"  第{i+1}行附近:\n{context}\n")
                                
                except Exception as e:
                    print(f"无法读取文件 {filepath}: {e}")
    
    print("=" * 80)
    print("搜索完成！")
    print("=" * 80)

def find_main_entry_points():
    """查找可能的入口文件"""
    print("\n" + "=" * 80)
    print("查找可能的入口点...")
    print("=" * 80)
    
    entry_files = ['run.py', 'main.py', 'app.py', 'server.py', 'start.py']
    
    for file in entry_files:
        if os.path.exists(file):
            print(f"\n✅ 找到入口文件: {file}")
            print("-" * 40)
            # 显示文件前30行
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for i, line in enumerate(lines[:30]):
                        print(f"{i+1:3d}: {line.rstrip()}")
            except Exception as e:
                print(f"无法读取文件: {e}")
        else:
            print(f"❌ 未找到: {file}")

if __name__ == "__main__":
    # 默认在当前目录搜索
    directory = sys.argv[1] if len(sys.argv) > 1 else "."
    
    find_main_entry_points()
    search_rag_functions(directory)
