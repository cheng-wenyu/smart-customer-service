#!/usr/bin/env python3
"""
最简单的AI代理服务
直接运行，无需虚拟环境
"""

from flask import Flask, request, jsonify
import requests
import json
import sys

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({"status": "ok", "service": "simple-ai-proxy"})

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        question = data.get('question', '')
        
        print(f"收到问题: {question[:100]}...", file=sys.stderr)
        
        # ========== 这里是你需要修改的部分 ==========
        # 方案1: 使用DeepSeek API（推荐）
        # 到 https://platform.deepseek.com/ 注册获取免费API密钥
        
        api_key = "sk-你的DeepSeek密钥"  # 替换为你的实际密钥
        
        response = requests.post(
            "https://api.deepseek.com/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "你是智能客服助手"},
                    {"role": "user", "content": question}
                ],
                "temperature": 0.7
            },
            timeout=30
        )
        
        if response.status_code == 200:
            answer = response.json()["choices"][0]["message"]["content"]
        else:
            answer = f"API调用失败: {response.status_code}"
            
        # 方案2: 如果你找到了本地模型，可以这样调用
        # response = requests.post(
        #     "http://localhost:8000/v1/chat/completions",
        #     json={"messages": [{"role": "user", "content": question}]}
        # )
        # answer = response.json()["choices"][0]["message"]["content"]
        
        # 方案3: 临时模拟回复（仅用于测试）
        # answer = f"我是智能客服，收到你的问题：{question}"
        # ===========================================
        
        return jsonify({
            "answer": answer,
            "status": "success"
        })
        
    except Exception as e:
        error_msg = f"错误: {str(e)}"
        print(error_msg, file=sys.stderr)
        return jsonify({
            "answer": error_msg,
            "status": "error"
        }), 500

if __name__ == '__main__':
    print("启动AI代理服务在端口 8001...", file=sys.stderr)
    app.run(host='0.0.0.0', port=8001, debug=False)
