import torch

print("🎯 PyTorch 包结构测试")
print("="*50)

# 查看torch的基本信息
print(f"1. PyTorch 版本: {torch.__version__}")
print(f"2. CUDA 是否可用: {torch.cuda.is_available()}")
print(f"3. 设备数量: {torch.cuda.device_count() if torch.cuda.is_available() else '无GPU'}")

# 测试基本功能
print("\n4. 张量运算测试:")
x = torch.tensor([1.0, 2.0, 3.0])
y = torch.tensor([4.0, 5.0, 6.0])
z = x + y
print(f"   {x} + {y} = {z}")

# 查看包路径
print(f"\n5. torch 包位置: {torch.__file__}")

# 尝试导入不存在的 pytorch 包
try:
    import pytorch
    print("6. ❌ 居然有 pytorch 包？")
except ImportError:
    print("6. ✅ 没有 pytorch 包（正确！应该用 import torch）")

print("\n🎉 结论：PyTorch 框架的 Python 包名是 torch")
