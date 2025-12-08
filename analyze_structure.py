import os
import sys
from pathlib import Path

def analyze_project(root_path="."):
    """分析项目结构"""
    print("📊 智能客服项目结构分析")
    print("="*60)
    
    root = Path(root_path)
    
    # 1. 总体统计
    py_files = list(root.rglob("*.py"))
    total_lines = 0
    for py_file in py_files:
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                total_lines += len(f.readlines())
        except:
            pass
    
    print(f"📁 项目根目录: {root.absolute()}")
    print(f"🐍 Python文件数: {len(py_files)}")
    print(f"📝 总代码行数: {total_lines}")
    
    # 2. 主要目录分析
    print("\n📂 主要目录结构:")
    for item in root.iterdir():
        if item.is_dir():
            size = sum(f.stat().st_size for f in item.rglob('*') if f.is_file())
            py_count = len(list(item.rglob("*.py")))
            print(f"  📁 {item.name}/")
            print(f"    大小: {size/1024/1024:.1f} MB")
            print(f"    Python文件: {py_count}")
    
    # 3. src目录详细分析
    src_dir = root / "src"
    if src_dir.exists():
        print("\n🔧 src/ 目录详细分析:")
        for py_file in src_dir.rglob("*.py"):
            if py_file.is_file():
                with open(py_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                # 分析导入
                imports = [line.strip() for line in lines if line.strip().startswith("import") or line.strip().startswith("from")]
                
                # 分析函数/类定义
                functions = [line.strip() for line in lines if line.strip().startswith("def ")]
                classes = [line.strip() for line in lines if line.strip().startswith("class ")]
                
                print(f"\n  📄 {py_file.relative_to(root)}")
                print(f"    行数: {len(lines)}")
                print(f"    函数: {len(functions)}")
                print(f"    类: {len(classes)}")
                print(f"    导入: {len(imports)}")
                
                # 显示前3个函数/类
                if functions:
                    print(f"    函数示例: {functions[0][:50]}...")
                if classes:
                    print(f"    类示例: {classes[0][:50]}...")

analyze_project()
