#!/usr/bin/env python3
# FastAPI AI客服服务

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import logging
import json
from datetime import datetime
import requests

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化FastAPI应用
app = FastAPI(
    title="智能客服系统",
    description="AI驱动的智能客服解决方案",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据模型
class ChatRequest(BaseModel):
    question: str
    session_id: str = None
    use_rag: bool = True  # 是否使用向量检索

class ChatResponse(BaseModel):
    answer: str
    status: str
    timestamp: str
    model: str = None

# ==================== AI模型配置 ====================

# 选择你的模型类型（修改这里）
MODEL_TYPE = "openai"  # 可选: openai, deepseek, zhipu, local

# 配置你的API密钥（这里填入你的密钥）
MODEL_CONFIG = {
    "openai": {
        "api_key": "sk-your-openai-key-here",
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-3.5-turbo"
    },
    "deepseek": {
        "api_key": "sk-your-deepseek-key-here",
        "base_url": "https://api.deepseek.com",
        "model": "deepseek-chat"
    },
    # 添加其他模型配置
}

def call_ai_model(question: str, context: str = "") -> str:
    """
    调用AI模型生成回答
    
    Args:
        question: 用户问题
        context: 可选的相关上下文
    
    Returns:
        AI生成的回答
    """
    try:
        if MODEL_TYPE == "openai":
            import openai
            openai.api_key = MODEL_CONFIG["openai"]["api_key"]
            openai.base_url = MODEL_CONFIG["openai"]["base_url"]
            
            messages = [
                {"role": "system", "content": "你是专业的智能客服助手，请友好、准确地回答用户问题。"},
                {"role": "user", "content": f"{context}\n\n问题：{question}" if context else question}
            ]
            
            response = openai.chat.completions.create(
                model=MODEL_CONFIG["openai"]["model"],
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
            
        elif MODEL_TYPE == "deepseek":
            headers = {
                "Authorization": f"Bearer {MODEL_CONFIG['deepseek']['api_key']}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": MODEL_CONFIG["deepseek"]["model"],
                "messages": [
                    {"role": "user", "content": question}
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            }
            
            response = requests.post(
                f"{MODEL_CONFIG['deepseek']['base_url']}/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
            
        elif MODEL_TYPE == "local":
            # 假设本地模型运行在7860端口
            response = requests.post(
                "http://localhost:7860/chat",
                json={"question": question},
                timeout=120
            )
            return response.json().get("answer", "未收到回答")
            
        else:
            return f"未知的模型类型: {MODEL_TYPE}"
            
    except Exception as e:
        logger.error(f"AI模型调用失败: {e}")
        return f"抱歉，暂时无法处理您的问题。错误信息：{str(e)}"

# ==================== API端点 ====================

@app.get("/")
async def root():
    """首页"""
    return {"message": "智能客服系统API服务", "status": "running"}

@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """聊天接口"""
    try:
        logger.info(f"收到问题: {request.question}")
        
        # 可选：从向量数据库检索相关知识（如果启用RAG）
        context = ""
        if request.use_rag:
            # 这里可以添加向量数据库检索逻辑
            context = retrieve_from_vector_db(request.question)
        
        # 调用AI模型
        answer = call_ai_model(request.question, context)
        
        logger.info(f"问题处理完成")
        
        return ChatResponse(
            answer=answer,
            status="success",
            timestamp=datetime.now().isoformat(),
            model=MODEL_TYPE
        )
        
    except Exception as e:
        logger.error(f"处理问题时出错: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def retrieve_from_vector_db(question: str) -> str:
    """从向量数据库检索相关文档"""
    # 这里可以集成ChromaDB
    # 暂时返回空字符串
    return ""

# ==================== 启动服务 ====================

if __name__ == "__main__":
    logger.info("🌐 启动Web服务...")
    logger.info(f"📍 服务地址: http://localhost:8000")
    logger.info(f"📚 API文档: http://localhost:8000/docs")
    logger.info(f"💬 聊天接口: http://localhost:8000/api/chat")
    logger.info(f"🤖 使用模型: {MODEL_TYPE}")
    logger.info("⏹️  按 Ctrl+C 停止服务")
    print("-"*50)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
