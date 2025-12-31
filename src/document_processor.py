#!/usr/bin/env python3
"""
文档处理器 - 使用已安装的库
功能：将长文档分割成适合AI处理的小文本
核心思想：大文档——>小片段——>更好的搜索效果
"""

import os
from typing import List

class DocumentProcessor:
    def __init__(self, chunk_size: int = 300):
        self.chunk_size = chunk_size
    
    def load_documents(self, file_path: str) -> List[str]:
        """加载文档并切分成块"""
        print("📖 正在加载文档...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 按空行分割段落
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        chunks = []
        for para in paragraphs:
            # 如果段落太长，进一步切分
            if len(para) > self.chunk_size:
                words = para.split()
                current_chunk = []
                current_length = 0
                
                for word in words:
                    if current_length + len(word) + 1 > self.chunk_size:
                        chunks.append(' '.join(current_chunk))
                        current_chunk = [word]
                        current_length = len(word)
                    else:
                        current_chunk.append(word)
                        current_length += len(word) + 1
                
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
            else:
                chunks.append(para)
        
        print(f"✅ 成功分割出 {len(chunks)} 个文本块")
        return chunks

# 测试这个模块
if __name__ == "__main__":
    processor = DocumentProcessor()
    chunks = processor.load_documents("data/return_policy.txt")
    
    print("\n前3个文本块预览：")
    for i, chunk in enumerate(chunks[:3]):
        print(f"块 {i+1}: {chunk[:80]}...")
