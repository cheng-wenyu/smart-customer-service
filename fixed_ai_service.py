#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import sys
from flask import Flask, request, jsonify
import requests
import urllib3

# 禁用SSL警告
urllib3.disable_warnings()

app = Flask(__name__)

# 配置你的DeepSeek API密钥
# 注册地址：https://platform.deepseek.com/
API_KEY = "sk-你的DeepSeek密钥"

def get_ai_response(question):
    """获取AI回答（修复编码问题）"""
    try:
        url = "https://api.deepseek.com/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json; charset=utf-8"  # 明确指定UTF-8
        }
        
        # 确保数据是UTF-8编码
        data = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system", 
                    "content": "你是专业的智能客服助手，用中文回答，保持友好、专业、有帮助。"
                },
                {
                    "role": "user", 
                    "content": question
                }
            ],
            "temperature": 0.7,
            "max_tokens": 2000,
            "stream": False
        }
        
        # 使用json.dumps确保编码正确
        json_data = json.dumps(data, ensure_ascii=False)
        
        response = requests.post(
            url, 
            headers=headers, 
            data=json_data.encode('utf-8'),  # 显式编码为UTF-8字节
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"API调用失败: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"请求失败: {str(e)}"

@app.route('/health')
def health():
    return jsonify({"status": "ok", "service": "fixed-ai-service"})

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        # 确保使用UTF-8解析请求
        if request.content_type == 'application/json':
            data = request.get_json()
        else:
            # 尝试直接解析原始数据
            raw_data = request.get_data(as_text=True)
            data = json.loads(raw_data)
        
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({"answer": "问题不能为空", "status": "error"})
        
        print(f"收到问题: {question}", file=sys.stderr, flush=True)
        
        # 获取回答
        answer = get_ai_response(question)
        
        print(f"返回答案，长度: {len(answer)}", file=sys.stderr, flush=True)
        
        return jsonify({
            "answer": answer,
            "status": "success",
            "timestamp": "2024-01-01T00:00:00"
        })
        
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr, flush=True)
        return jsonify({
            "answer": f"处理请求时出错: {str(e)}",
            "status": "error"
        }), 500

if __name__ == '__main__':
    print("启动AI服务 (UTF-8 修复版) 在 0.0.0.0:8001", file=sys.stderr, flush=True)
    app.run(host='0.0.0.0', port=8001, debug=False)
