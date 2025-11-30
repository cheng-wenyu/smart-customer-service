#!/usr/bin/env python3
"""
批量测试问题
"""

import requests
import json

# API地址
BASE_URL = "http://localhost:8000"

def test_question(question):
    """测试单个问题"""
    try:
        response = requests.post(
            f"{BASE_URL}/ask",
            json={"question": question, "top_k": 3}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"❓ 问题: {result['question']}")
            print(f"🤖 回答: {result['answer']}")
            print(f"📄 相关文档: {len(result['relevant_documents'])} 个")
            for i, doc in enumerate(result['relevant_documents']):
                print(f"   {i+1}. {doc[:80]}...")
            print("-" * 80)
        else:
            print(f"❌ 请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 错误: {e}")

def main():
    """测试多个问题"""
    questions = [
        "退货需要几天时间",
        "客服电话是多少",
        "什么商品不能退",
        "运费谁承担", 
        "退款多久到账",
        "怎么申请退货",
        "生鲜食品能退吗",
        "工作时间是什么时候"
    ]
    
    print("🧪 开始测试智能客服系统...\n")
    
    for question in questions:
        test_question(question)

if __name__ == "__main__":
    main()
