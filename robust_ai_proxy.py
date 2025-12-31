#!/usr/bin/env python3
import flask
from flask import Flask, request, jsonify
import requests
import traceback
import sys

app = Flask(__name__)

# 配置
API_KEY = "sk-你的DeepSeek密钥"  # 请替换为你的实际密钥

def get_ai_response(question):
    """获取AI回复"""
    try:
        # 使用DeepSeek API
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "你是一个智能客服助手，回答要友好、专业、有帮助。"},
                {"role": "user", "content": question}
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        response = requests.post(
            "https://api.deepseek.com/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"API调用失败: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"请求失败: {str(e)}"

@app.route('/health')
def health():
    return jsonify({"status": "ok", "service": "robust-ai-proxy"})

@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def chat():
    """处理聊天请求"""
    if request.method == 'OPTIONS':
        # 处理CORS预检请求
        return jsonify({}), 200
    
    try:
        data = request.json
        if not data:
            return jsonify({"answer": "请求数据为空", "status": "error"}), 400
            
        question = data.get('question', '').strip()
        if not question:
            return jsonify({"answer": "问题内容不能为空", "status": "error"}), 400
        
        print(f"处理问题: {question[:50]}...", file=sys.stderr)
        
        # 获取AI回复
        answer = get_ai_response(question)
        
        print(f"回复长度: {len(answer)}", file=sys.stderr)
        
        return jsonify({
            "answer": answer,
            "status": "success",
            "timestamp": "2024-01-01T00:00:00"
        })
        
    except Exception as e:
        error_msg = f"服务器错误: {str(e)}\n{traceback.format_exc()}"
        print(error_msg, file=sys.stderr)
        return jsonify({
            "answer": f"处理请求时出错: {str(e)}",
            "status": "error"
        }), 500

if __name__ == '__main__':
    print("启动AI代理服务在 0.0.0.0:8001", file=sys.stderr)
    app.run(host='0.0.0.0', port=8001, debug=False, threaded=True)
