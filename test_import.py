import sys
import os

print("当前工作目录:", os.getcwd())
print("Python路径:")
for p in sys.path[:5]:
    print(" ", p)

print("\n尝试导入...")
try:
    # 尝试1：绝对导入
    from src.api_service import main
    print("✅ 绝对导入成功")
except ImportError as e:
    print("❌ 绝对导入失败:", e)

try:
    # 尝试2：直接导入（假设在src目录）
    import sys
    sys.path.insert(0, 'src')
    from api_service import main
    print("✅ 直接导入成功")
except ImportError as e:
    print("❌ 直接导入失败:", e)
