#!/usr/bin/env python3
"""
AI代理服务 - 将Web界面的请求转发到AI模型
运行在 8001 端口，然后通过Nginx反向代理到5000端口的/api/chat路径
"""

from flask import Flask, request, jsonify
import requests
import json
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# ========== 配置你的AI模型 ==========
# 选择1: DeepSeek API（免费，推荐）
# 到 https://platform.deepseek.com/ 注册获取API密钥
DEEPSEEK_API_KEY = "sk-你的DeepSeek密钥"
DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"

# 选择2: 本地模型（如果你有）
# LOCAL_MODEL_URL = "http://localhost:7860/chat"

def call_deepseek(question):
    """调用DeepSeek API"""
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system", 
                "content": "你是专业的智能客服助手，回答要友好、准确、有帮助。"
            },
            {"role": "user", "content": question}
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"API调用失败: {response.status_code} - {response.text}"
    except Exception as e:
        return f"请求失败: {str(e)}"

def call_local_model(question):
    """调用本地模型（如果你有）"""
    try:
        response = requests.post(
            "http://localhost:7860/chat",
            json={"question": question},
            timeout=30
        )
        if response.status_code == 200:
            return response.json().get("answer", "未收到回答")
        else:
            return "本地模型服务异常"
    except:
        return "无法连接到本地模型"

@app.route('/health')
def health():
    return jsonify({"status": "ok", "service": "ai-proxy"})

@app.route('/api/chat', methods=['POST'])
def chat():
    """聊天接口 - 与Web界面兼容"""
    try:
        data = request.json
        question = data.get('question', '')
        
        if not question:
            return jsonify({"answer": "请提供问题内容", "status": "error"})
        
        logger.info(f"收到问题: {question[:50]}...")
        
        # 调用AI模型（这里使用DeepSeek，你可以切换）
        answer = call_deepseek(question)
        # 如果想用本地模型：answer = call_local_model(question)
        
        logger.info(f"返回答案，长度: {len(answer)}")
        
        return jsonify({
            "answer": answer,
            "status": "success",
            "timestamp": "2024-01-01T00:00:00"  # 简化版
        })
        
    except Exception as e:
        logger.error(f"处理请求失败: {e}")
        return jsonify({
            "answer": f"处理请求时出错: {str(e)}",
            "status": "error"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=False)
