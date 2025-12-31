import torch
from sentence_transformers import SentenceTransformer

print("🤖 智能问答系统测试")
print("="*50)

# 1. 测试PyTorch
print("1. PyTorch 测试:")
x = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
print(f"   创建张量: {x.shape}")
print(f"   设备: {'GPU' if torch.cuda.is_available() else 'CPU'}")

# 2. 测试sentence-transformers
print("\n2. sentence-transformers 测试:")
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
embeddings = model.encode("你好，智能客服")
print(f"   文本向量维度: {len(embeddings)}")

# 3. 简单的问答测试
print("\n3. 智能问答测试:")
questions = ["怎么退货", "物流时间", "客服电话"]
for q in questions:
    vec = model.encode(q)
    print(f"   '{q}' → 向量长度: {len(vec)}")

print("\n🎉 所有测试通过！可以开始构建智能客服了。")
