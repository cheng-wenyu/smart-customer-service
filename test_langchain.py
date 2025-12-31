#!/usr/bin/env python3
"""
测试LangChain基本功能
"""
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

print("🧪 开始测试LangChain...")

# 测试文档加载
try:
    loader = TextLoader("data/return_policy.txt")
    documents = loader.load()
    print(f"✅ 成功加载 {len(documents)} 个文档")
    
    # 测试文本分割
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=50
    )
    texts = text_splitter.split_documents(documents)
    print(f"✅ 成功分割为 {len(texts)} 个文本块")
    
    print("🎉 LangChain测试通过！")
    
except Exception as e:
    print(f"❌ LangChain测试失败: {e}")
