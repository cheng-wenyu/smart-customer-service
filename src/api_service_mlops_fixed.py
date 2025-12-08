#!/usr/bin/env python3
"""
MLOps监控版服务 - 修复版本
"""

import sys
import os
import time
import logging
from datetime import datetime
from typing import List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

# ========== 添加监控相关导入 ==========
from prometheus_client import (
    Counter, Histogram, Gauge, generate_latest, 
    CONTENT_TYPE_LATEST, REGISTRY, start_http_server
)
import psutil
import json

# ========== 先定义所有指标 ==========
# 请求相关指标
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status_code']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency in seconds',
    ['method', 'endpoint']
)

# 业务相关指标
RAG_QUERY_COUNT = Counter(
    'rag_queries_total',
    'Total RAG queries processed',
    ['query_type']
)

RAG_QUERY_LATENCY = Histogram(
    'rag_query_duration_seconds',
    'RAG query processing latency in seconds',
    ['query_type']
)

# 系统资源指标
CPU_USAGE = Gauge('system_cpu_usage_percent', 'System CPU usage percentage')
MEMORY_USAGE = Gauge('system_memory_usage_percent', 'System memory usage percentage')
ACTIVE_CONNECTIONS = Gauge('active_connections', 'Number of active connections')

# ========== 系统状态监控 ==========
def get_system_metrics():
    """收集系统指标"""
    CPU_USAGE.set(psutil.cpu_percent(interval=1))
    MEMORY_USAGE.set(psutil.virtual_memory().percent)
    
    # 获取网络连接数（简化版）
    connections = len(psutil.net_connections())
    ACTIVE_CONNECTIONS.set(connections)
    
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "active_connections": connections,
        "timestamp": datetime.now().isoformat()
    }

# ========== 数据模型 ==========
class Question(BaseModel):
    question: str
    top_k: Optional[int] = 3

class Answer(BaseModel):
    question: str
    answer: str
    relevant_documents: List[str]
    processing_time: float
    model_version: str = "1.0.0"

# ========== FastAPI应用生命周期 ==========
@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    print("🚀 启动智能客服系统（MLOps监控版）...")
    
    # 启动Prometheus指标服务器（在8001端口）
    start_http_server(8001)
    print("📊 Prometheus指标服务器启动在端口 8001")
    
    yield  # 应用运行中
    
    # 关闭时
    print("🛑 正在关闭智能客服系统...")

# ========== 创建FastAPI应用 ==========
app = FastAPI(
    title="智能客服系统 - MLOps增强版",
    description="带有完整监控的RAG系统",
    version="2.0.0",
    lifespan=lifespan
)

# ========== 中间件：收集请求指标（现在放在app定义之后） ==========
@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    start_time = time.time()
    method = request.method
    endpoint = request.url.path
    
    try:
        response = await call_next(request)
        
        # 记录请求指标
        REQUEST_COUNT.labels(
            method=method,
            endpoint=endpoint,
            status_code=response.status_code
        ).inc()
        
        REQUEST_LATENCY.labels(
            method=method,
            endpoint=endpoint
        ).observe(time.time() - start_time)
        
        return response
        
    except Exception as e:
        REQUEST_COUNT.labels(
            method=method,
            endpoint=endpoint,
            status_code=500
        ).inc()
        raise e

# ========== API端点 ==========
@app.get("/")
async def root():
    """根端点"""
    return {
        "service": "智能客服系统",
        "version": "2.0.0",
        "status": "running",
        "monitoring": {
            "metrics": "http://localhost:8000/metrics",
            "health": "http://localhost:8000/health",
            "docs": "http://localhost:8000/docs"
        }
    }

@app.get("/health")
async def health_check():
    """健康检查端点（MLOps标准）"""
    system_status = get_system_metrics()
    
    # 检查关键组件
    checks = {
        "api_service": "healthy",
        "system_resources": "healthy" if system_status["cpu_percent"] < 90 else "warning",
        "database": "healthy",  # 这里可以添加实际的数据库检查
        "model_serving": "healthy"
    }
    
    overall_status = "healthy" if all(v == "healthy" for v in checks.values()) else "degraded"
    
    return {
        "status": overall_status,
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "checks": checks,
        "system": system_status
    }

@app.get("/metrics")
async def metrics():
    """Prometheus指标端点"""
    # 更新系统指标
    get_system_metrics()
    
    # 返回所有指标
    return Response(
        generate_latest(REGISTRY),
        media_type=CONTENT_TYPE_LATEST
    )

@app.get("/system/status")
async def system_status():
    """详细系统状态"""
    return {
        "status": "running",
        "uptime": "TODO: 计算运行时间",
        "resources": get_system_metrics(),
        "service_info": {
            "name": "智能客服系统",
            "version": "2.0.0",
            "mlops_features": ["监控", "指标", "健康检查", "日志"],
            "rag_features": ["文档检索", "向量搜索", "智能问答"]
        }
    }

@app.post("/ask", response_model=Answer)
async def ask(question: Question):
    """智能问答端点（带监控）"""
    start_time = time.time()
    
    try:
        # 记录查询
        RAG_QUERY_COUNT.labels(query_type="general").inc()
        
        # 这里可以调用你的RAG逻辑
        # 暂时用模拟数据
        answer = "这是模拟回答：根据退货政策，商品签收后7天内可无理由退货，商品必须保持完好，标签未拆除。"
        relevant_docs = [
            "商品签收后7天内可无理由退货",
            "商品必须保持完好，标签未拆除",
            "退货运费由买家承担"
        ]
        
        processing_time = time.time() - start_time
        
        # 记录延迟
        RAG_QUERY_LATENCY.labels(query_type="general").observe(processing_time)
        
        return Answer(
            question=question.question,
            answer=answer,
            relevant_documents=relevant_docs,
            processing_time=round(processing_time, 3)
        )
        
    except Exception as e:
        RAG_QUERY_COUNT.labels(query_type="error").inc()
        raise HTTPException(status_code=500, detail=str(e))

# ========== 错误处理 ==========
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理"""
    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc),
            "timestamp": datetime.now().isoformat(),
            "path": request.url.path
        }
    )

# ========== 启动应用 ==========
if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("=" * 60)
    print("🌐 MLOps智能客服系统")
    print("📍 API服务: http://localhost:8000")
    print("📊 指标地址: http://localhost:8000/metrics")
    print("📚 API文档: http://localhost:8000/docs")
    print("🔬 内部指标: http://localhost:8001")
    print("=" * 60)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        access_log=True
    )
