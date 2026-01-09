# src/llm_generator.py
import os
import logging
from typing import List
from openai import OpenAI

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化客户端 - 从环境变量读取密钥
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    logger.error("DEEPSEEK_API_KEY 环境变量未设置！")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com",  # DeepSeek的API端点
    timeout=30.0  # 设置超时
)

def generate_answer(question: str, contexts: List[str]) -> str:
    """
    使用DeepSeek API生成基于上下文的答案
    """
    if not contexts:
        return "抱歉，没有找到相关信息来回答您的问题。"
    
    # 构建优化的跨境电商客服Prompt
    prompt = f"""你是一位专业的跨境电商客服助理。请严格根据以下【已知信息】来回答用户的【问题】。

【已知信息】：
{chr(10).join(['• ' + ctx for ctx in contexts])}

【用户问题】：
{question}

【回答要求】：
1. 回答必须完全依据【已知信息】，不要编造未知内容。
2. 如果信息不足，请说“根据现有信息，无法完整回答此问题，建议您联系人工客服”。
3. 回答简洁、专业、友好，使用中文。
4. 如果涉及步骤，请分点说明。

请开始回答："""
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",  # 指定模型
            messages=[
                {"role": "system", "content": "你是一位专业的跨境电商客服助手，专注于根据提供的信息准确回答问题。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # 平衡创造性和确定性
            max_tokens=500    # 控制回答长度
            max_tokens=200  # 新增：限制生成回答的长度，节约token
        )
        answer = response.choices[0].message.content
        logger.info(f"成功生成回答，消耗Token数: {response.usage.total_tokens if response.usage else '未知'}")
        return answer
        
    except Exception as e:
        logger.error(f"调用DeepSeek API失败: {e}")
        # 提供一个友好的降级回答
        return "系统正在升级服务，请稍后再试或联系人工客服。"
