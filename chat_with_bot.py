#!/usr/bin/env python3
"""
与智能客服对话的友好界面
"""

import requests
import json

class CustomerServiceBot:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.conversation_history = []
    
    def print_welcome(self):
        """显示欢迎信息"""
        print("🤖" * 50)
        print("           欢迎使用智能客服系统")
        print("🤖" * 50)
        print()
        print("我可以回答关于退货政策、退款流程、联系方式等问题")
        print("输入 'quit' 或 '退出' 结束对话")
        print("-" * 60)
    
    def ask_question(self, question):
        """向客服系统提问"""
        try:
            response = requests.post(
                f"{self.base_url}/ask",
                json={"question": question, "top_k": 3},
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"请求失败: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"连接错误: {e}"}
    
    def format_response(self, result):
        """格式化回答，让输出更友好"""
        if "error" in result:
            return f"❌ {result['error']}"
        
        response = f"💬 {result['answer']}\n"
        
        if result['relevant_documents']:
            response += f"\n📚 参考信息 ({len(result['relevant_documents'])}条):\n"
            for i, doc in enumerate(result['relevant_documents'], 1):
                # 清理文档显示
                clean_doc = ' '.join(doc.split())
                if len(clean_doc) > 80:
                    clean_doc = clean_doc[:80] + "..."
                response += f"   {i}. {clean_doc}\n"
        
        return response
    
    def start_chat(self):
        """开始对话"""
        self.print_welcome()
        
        while True:
            try:
                # 获取用户输入
                question = input("\n🙋 你的问题: ").strip()
                
                if question.lower() in ['quit', '退出', 'exit', 'q']:
                    print("\n👋 感谢使用，再见！")
                    break
                
                if not question:
                    print("⚠️  请输入问题")
                    continue
                
                print("🔄 正在查询...")
                
                # 获取回答
                result = self.ask_question(question)
                
                # 显示结果
                print("\n" + self.format_response(result))
                
                # 记录对话历史
                self.conversation_history.append({
                    "question": question,
                    "answer": result.get('answer', '') if not result.get('error') else result['error']
                })
                
            except KeyboardInterrupt:
                print("\n\n👋 对话结束")
                break
            except Exception as e:
                print(f"❌ 发生错误: {e}")

if __name__ == "__main__":
    # 检查服务是否运行
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            bot = CustomerServiceBot()
            bot.start_chat()
        else:
            print("❌ 客服系统服务异常")
    except:
        print("❌ 无法连接到客服系统")
        print("💡 请确保已在另一个终端中运行: python src/api_service_final.py")
