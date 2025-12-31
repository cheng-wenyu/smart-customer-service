#!/usr/bin/env python3
"""
LangChain修复版本的API服务 - 支持最新版本
"""

import sys
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

# LangChain 1.x版本的导入方式
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI  # 或使用其他LLM
from langchain.callbacks import StdOutCallbackHandler

app = FastAPI(title="智能客服系统 (LangChain 1.x版)")

# 数据模型
class QuestionRequest(BaseModel):
    question: str
    top_k: Optional[int] = 3

class QuestionResponse(BaseModel):
    question: str
    answer: str
    relevant_documents: List[str]

# 全局变量
vector_store = None
retriever = None

def initialize_system():
    """初始化系统 - LangChain版本"""
    global vector_store, retriever
    
    print("🚀 正在使用LangChain 1.x初始化系统...")
    
    # 1. 加载文档
    try:
        loader = TextLoader("data/return_policy.txt")
        documents = loader.load()
        print(f"📖 加载了 {len(documents)} 个文档")
    except Exception as e:
        print(f"❌ 文档加载失败: {e}")
        # 备选方案：使用简单文件读取
        with open("data/return_policy.txt", "r", encoding="utf-8") as f:
            text = f.read()
        from langchain.schema import Document
        documents = [Document(page_content=text, metadata={"source": "return_policy"})]
        print(f"📖 使用备选方案加载文档")
    
    # 2. 分割文本
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
        length_function=len,
        separators=["\n\n", "\n", "。", "！", "？", "；", "，", "、", " "]
    )
    
    texts = text_splitter.split_documents(documents)
    print(f"✂️ 分割为 {len(texts)} 个文本块")
    
    # 3. 创建向量存储
    try:
        # 使用更兼容的Embedding模型
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
        
        # 创建Chroma向量存储
        vector_store = Chroma.from_documents(
            documents=texts,
            embedding=embeddings,
            persist_directory="./chroma_db_langchain"
        )
        
        # 创建检索器
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})
        
        print("✅ LangChain系统初始化完成")
        
    except Exception as e:
        print(f"❌ 向量存储创建失败: {e}")
        print("⚠️ 使用简单的内存检索器作为备选")
        from langchain.retrievers import BM25Retriever
        retriever = BM25Retriever.from_documents(texts)

# 启动时初始化
initialize_system()

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "LangChain 1.x版服务运行正常"}

@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    try:
        print(f"📨 收到问题: {request.question}")
        
        # 使用检索器获取相关文档
        relevant_docs = retriever.invoke(request.question)
        
        # 构建简单答案
        if relevant_docs:
            answer = f"根据相关政策，找到了以下相关信息："
            doc_contents = [doc.page_content[:200] + "..." for doc in relevant_docs[:request.top_k]]
        else:
            answer = "抱歉，未找到相关信息。"
            doc_contents = []
        
        return QuestionResponse(
            question=request.question,
            answer=answer,
            relevant_documents=doc_contents
        )
        
    except Exception as e:
        print(f"❌ 处理问题时出错: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("🌐 启动LangChain版Web服务...")
    print("📍 服务地址: http://localhost:8001")
    print("📚 API文档: http://localhost:8001/docs")
    print("⏹️  按 Ctrl+C 停止服务")
    print("--------------------------------------------------")
    uvicorn.run(app, host="0.0.0.0", port=8001)
