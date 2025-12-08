#!/usr/bin/env python3
"""
修复 VectorSearch 初始化问题
"""
import re

# 读取 api_service.py
with open('src/api_service.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 查找并替换 initialize() 调用
# 根据 vector_search.py 的实际方法修改

# 先尝试最简单的修复：去掉 initialize() 调用
# 因为初始化可能在 __init__ 中已经完成了
new_content = re.sub(
    r'vector_search = VectorSearch\(\)\s*\n\s*vector_search\.initialize\(\)',
    'vector_search = VectorSearch()',
    content
)

# 如果上面的替换没生效，尝试其他方式
if new_content == content:
    # 替换为可能的其他方法名
    new_content = re.sub(
        r'vector_search\.initialize\(\)',
        '# vector_search.initialize()  # 已移除，因为在 __init__ 中初始化',
        content
    )

# 写回文件
with open('src/api_service.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ 已修复 initialize() 问题")
print("   如果还有问题，请检查 vector_search.py 的实际方法名")
