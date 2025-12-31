#!/usr/bin/env python3
"""
最终修复版本的API服务
"""

import sys
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

# 添加src目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

# 现在可以正常导入
from src.document_processor import DocumentProcessor
from src.vector_search import VectorSearch

# 创建FastAPI应用
app = FastAPI(
    title="智能客服系统",
    description="基于RAG架构的智能客服问答系统",
    version="1.0.0"
)

# 全局变量
search_system = None
processor = None

class QuestionRequest(BaseModel):
    question: str
    top_k: Optional[int] = 3

class AnswerResponse(BaseModel):
    question: str
    answer: str
    relevant_documents: List[str]
    success: bool

@app.on_event("startup")
async def startup_event():
    """服务启动时初始化系统"""
    global search_system, processor
    
    print("🚀 正在启动智能客服系统...")
    
    try:
        # 1. 初始化文档处理器
        processor = DocumentProcessor()
        
        # 2. 构建正确的数据文件路径
        data_path = os.path.join(project_root, "data", "return_policy.txt")
        print(f"📁 数据文件路径: {data_path}")
        
        # 3. 加载文档
        documents = processor.load_documents(data_path)
        
        # 4. 初始化向量搜索系统
        search_system = VectorSearch()
        
        # 5. 将文档添加到向量数据库
        search_system.add_documents(documents)
        
        print("✅ 智能客服系统启动完成！")
        
    except Exception as e:
        print(f"❌ 系统启动失败: {e}")
        import traceback
        traceback.print_exc()
        raise

@app.get("/")
async def root():
    return {
        "message": "欢迎使用智能客服系统！",
        "version": "1.0.0",
        "status": "运行正常",
        "endpoints": {
            "health": "/health",
            "ask": "/ask (POST)",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "smart-customer-service",
        "components": {
            "vector_database": "ready",
            "embedding_model": "ready"
        }
    }

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    try:
        print(f"📨 收到问题: {request.question}")
        
        # 搜索相关文档
        relevant_docs = search_system.search(request.question, request.top_k)
        
        # 生成回答
        if relevant_docs:
            answer = generate_simple_answer(request.question, relevant_docs)
            success = True
        else:
            answer = "抱歉，我没有找到相关的政策信息。请尝试换一种方式提问，或联系人工客服。"
            success = False
        
        return AnswerResponse(
            question=request.question,
            answer=answer,
            relevant_documents=relevant_docs,
            success=success
        )
        
    except Exception as e:
        print(f"❌ 处理问题时出错: {e}")
        raise HTTPException(status_code=500, detail=f"处理问题时出错: {str(e)}")

def generate_simple_answer(question: str, relevant_docs: List[str]) -> str:
    """简单的回答生成函数"""
    # 将相关文档拼接起来
    context = "\n".join([f"- {doc}" for doc in relevant_docs])
    
    # 基于问题和上下文生成回答
    if "退货" in question or "退款" in question:
        answer = f"关于您的问题，我们的政策是：\n{context}\n\n如果您需要进一步帮助，请联系客服。"
    elif "联系" in question or "客服" in question:
        answer = f"我们的联系方式：\n{context}\n\n服务时间请参考上述信息。"
    else:
        answer = f"根据我们的政策信息：\n{context}\n\n如果您需要更详细的帮助，请联系客服。"
    
    return answer

def run_service():
    """启动Web服务"""
    print("🌐 启动Web服务...")
    print("📍 服务地址: http://localhost:8000")
    print("📚 API文档: http://localhost:8000/docs")
    print("⏹️  按 Ctrl+C 停止服务")
    print("-" * 50)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    run_service()
