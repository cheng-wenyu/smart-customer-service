"""
配置文件
"""
import os
from dataclasses import dataclass

@dataclass
class Config:
    """系统配置"""
    # API配置
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", 8000))
    
    # 向量搜索配置
    VECTOR_DB_PATH: str = os.getenv("VECTOR_DB_PATH", "./data/vectors")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
    TOP_K_RESULTS: int = int(os.getenv("TOP_K_RESULTS", 3))
    
    # 对话配置
    MAX_CONVERSATION_HISTORY: int = 10
    CONFIDENCE_THRESHOLD: float = 0.5
    
    # 模型路径（本地模型）
    LOCAL_MODEL_PATH: str = os.getenv("LOCAL_MODEL_PATH", "./models")
    
    @classmethod
    def from_env(cls):
        """从环境变量加载配置"""
        return cls()

# 全局配置实例
config = Config.from_env()
