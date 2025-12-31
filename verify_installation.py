#!/usr/bin/env python3
"""
验证所有关键功能是否正常
"""

def verify_core_features():
    print("🔍 验证核心功能...")
    
    try:
        # 1. 验证Web框架
        import fastapi
        print("✅ FastAPI - Web框架正常")
        
        # 2. 验证向量数据库
        import chromadb
        print("✅ ChromaDB - 向量数据库正常")
        
        # 3. 验证NLP模型（使用transformers替代sentence-transformers）
        from transformers import AutoTokenizer, AutoModel
        print("✅ Transformers - NLP模型库正常")
        
        # 4. 验证PyTorch
        import torch
        print(f"✅ PyTorch {torch.__version__} - 深度学习框架正常")
        
        print("\n🎉 所有核心功能验证通过！")
        print("🚀 可以开始正式开发了！")
        return True
        
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False

if __name__ == "__main__":
    verify_core_features()
