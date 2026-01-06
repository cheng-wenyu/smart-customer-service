#!/usr/bin/env python
"""
自动下载所需模型的脚本
"""
import os
import sys
import time
from huggingface_hub import snapshot_download

def download_model_with_retry(repo_id, local_dir, retries=3):
    """带重试的模型下载"""
    for attempt in range(retries):
        try:
            print(f"尝试下载模型 {repo_id} (尝试 {attempt + 1}/{retries})")
            
            # 设置镜像源
            if 'HF_ENDPOINT' not in os.environ:
                os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
            
            # 下载模型
            snapshot_download(
                repo_id=repo_id,
                local_dir=local_dir,
                resume_download=True,
                local_files_only=False
            )
            
            print(f"✅ 模型 {repo_id} 下载成功")
            return True
            
        except Exception as e:
            print(f"❌ 下载失败: {e}")
            if attempt < retries - 1:
                wait_time = (attempt + 1) * 30  # 等待时间递增
                print(f"等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
            else:
                print(f"❌ 模型 {repo_id} 下载失败，已尝试 {retries} 次")
                return False
    return False

def main():
    """下载所有需要的模型"""
    models_to_download = [
        {
            "repo_id": "BAAI/bge-small-zh",
            "local_dir": "/app/models/bge-small-zh"
        },
        # 可以根据需要添加更多模型
    ]
    
    print("开始下载模型...")
    
    for model in models_to_download:
        success = download_model_with_retry(
            repo_id=model["repo_id"],
            local_dir=model["local_dir"]
        )
        
        if not success:
            print(f"警告: 模型 {model['repo_id']} 下载失败，可能会影响功能")
    
    print("模型下载完成")

if __name__ == "__main__":
    main()
