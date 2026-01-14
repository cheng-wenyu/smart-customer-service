#!/usr/bin/env python3
"""
向量搜索模块 - 使用ChromaDB和Transformers
"""

import os
import chromadb
import sys
import logging
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
from typing import List
from .document_processor import DocumentProcessor

#logger.debug(f"向量搜索输入: {question}")
#logger.debug(f"向量搜索输出: {len(results)} 个结果")


class VectorSearch:
    def __init__(self, persist_directory: str = "./chroma_db"):
        """
        初始化向量搜索系统
        """
        print("🔄 初始化向量搜索系统...")
        
        # 初始化ChromaDB向量数据库
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(
            name="customer_service_knowledge"
        )
        
        # 加载中文嵌入模型
        print("🔄 加载嵌入模型...")
        self.tokenizer = AutoTokenizer.from_pretrained('/app/data/models/bge-small-zh')
        self.model = AutoModel.from_pretrained('/app/data/models/bge-small-zh')
        
        # 设置模型为评估模式
        self.model.eval()
        
        print("✅ 向量搜索系统初始化完成")
    
    def get_embedding(self, text: str) -> List[float]:
        """
        将文本转换为向量嵌入
        """
        # 对输入文本进行编码
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        
        # 生成嵌入
        with torch.no_grad():
            outputs = self.model(**inputs)
            # 使用[CLS] token的嵌入作为句子表示
            embedding = outputs.last_hidden_state[:, 0, :].squeeze().numpy()
        
        return embedding.tolist()
    
    def add_documents(self, documents: List[str]):
        """
        将文档添加到向量数据库
        """
        # 清空现有集合，避免重复添加
        try:
            self.collection.delete(where={})
        except:
            pass
        print(f"📝 正在处理 {len(documents)} 个文档...")
        
        # 为每个文档生成嵌入
        embeddings = []
        for i, doc in enumerate(documents):
            if i % 10 == 0:  # 每10个文档打印一次进度
                print(f"  生成嵌入进度: {i}/{len(documents)}")
            embedding = self.get_embedding(doc)
            embeddings.append(embedding)
        
        # 为文档创建ID
        ids = [f"doc_{i}" for i in range(len(documents))]
        
        # 添加到向量数据库
        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            ids=ids
        )
        
        print(f"🎉 成功将 {len(documents)} 个文档添加到向量数据库")
    
    def search(self, query: str, top_k: int = config.TOP_K_RESULTS) -> List[str]:
        """
        搜索最相关的文档
        """
        print(f"🔍 正在搜索: '{query}'")
        
        # 将查询转换为嵌入
        query_embedding = self.get_embedding(query)
        
        # 在向量数据库中搜索
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        if results['documents']:
            relevant_docs = results['documents'][0]
            print(f"✅ 找到 {len(relevant_docs)} 个相关结果")
            return relevant_docs
        else:
            print("❌ 没有找到相关结果")
            return []

def demo_vector_search():
    """演示向量搜索功能"""
    print("=== 向量搜索演示 ===\n")
    
    # 1. 加载文档
    processor = DocumentProcessor()
    documents = processor.load_documents("data/return_policy.txt")
    
    # 2. 初始化向量搜索
    searcher = VectorSearch()
    
    # 3. 添加文档到向量数据库
    searcher.add_documents(documents)
    
    # 4. 测试搜索功能
    test_queries = [
        "退货需要几天时间",
        "怎么联系客服",
        "什么商品不能退货",
        "运费谁承担"
    ]
    
    for query in test_queries:
        print(f"\n{'='*50}")
        print(f"问题: {query}")
        
        results = searcher.search(query)
        
        for i, result in enumerate(results):
            print(f"\n相关结果 {i+1}:")
            print(result)
        
        print(f"{'='*50}")

if __name__ == "__main__":
    demo_vector_search()
