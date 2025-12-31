print("🚀 测试智能客服开发环境...\n")

# 测试sentence-transformers
try:
    from sentence_transformers import SentenceTransformer
    print("✅ sentence-transformers 版本:", SentenceTransformer.__version__)
    
    # 测试一个小模型
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    embeddings = model.encode("你好，智能客服")
    print("✅ 模型测试成功，向量维度:", len(embeddings))
except Exception as e:
    print("❌ sentence-transformers 错误:", e)

print()

# 测试torch
try:
    import torch
    print("✅ PyTorch 版本:", torch.__version__)
    print("✅ CUDA 可用:", torch.cuda.is_available())
except Exception as e:
    print("❌ PyTorch 错误:", e)

print()

# 测试langchain
try:
    from langchain.embeddings import HuggingFaceEmbeddings
    print("✅ LangChain 导入成功")
except Exception as e:
    print("❌ LangChain 错误:", e)
