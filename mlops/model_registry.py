#!/usr/bin/env python3
"""
简单的模型注册表
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path

class ModelRegistry:
    def __init__(self, registry_path="models/registry"):
        self.registry_path = Path(registry_path)
        self.registry_path.mkdir(parents=True, exist_ok=True)
        
    def register_model(self, model_name, model_path, metadata=None):
        """注册新模型版本"""
        version = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_dir = self.registry_path / model_name / version
        
        # 创建版本目录
        model_dir.mkdir(parents=True, exist_ok=True)
        
        # 复制模型文件
        if os.path.isdir(model_path):
            shutil.copytree(model_path, model_dir, dirs_exist_ok=True)
        else:
            shutil.copy(model_path, model_dir)
        
        # 保存元数据
        metadata = metadata or {}
        metadata.update({
            "name": model_name,
            "version": version,
            "register_time": datetime.now().isoformat(),
            "path": str(model_dir)
        })
        
        with open(model_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
        
        # 更新最新版本链接
        latest_link = self.registry_path / model_name / "latest"
        if latest_link.exists():
            latest_link.unlink()
        latest_link.symlink_to(version)
        
        print(f"✅ 注册模型: {model_name} v{version}")
        return version
    
    def get_model(self, model_name, version="latest"):
        """获取模型路径"""
        if version == "latest":
            model_dir = self.registry_path / model_name / "latest"
        else:
            model_dir = self.registry_path / model_name / version
        
        if not model_dir.exists():
            raise FileNotFoundError(f"模型不存在: {model_name}/{version}")
        
        return model_dir
    
    def list_models(self):
        """列出所有模型"""
        models = {}
        for model_dir in self.registry_path.iterdir():
            if model_dir.is_dir():
                versions = []
                for version_dir in model_dir.iterdir():
                    if version_dir.is_dir() and version_dir.name != "latest":
                        versions.append(version_dir.name)
                models[model_dir.name] = sorted(versions, reverse=True)
        return models

if __name__ == "__main__":
    registry = ModelRegistry()
    print("📋 已注册模型:")
    for model, versions in registry.list_models().items():
        print(f"  {model}: {versions[:3]}...")
