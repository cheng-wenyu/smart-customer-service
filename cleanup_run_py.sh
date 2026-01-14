#!/bin/bash

echo "=== 清理 run.py 及相关文件 ==="
echo

# 1. 检查 run.py 是否存在
if [ ! -f "run.py" ]; then
    echo "❌ run.py 已不存在"
    exit 1
fi

# 2. 显示 run.py 内容预览
echo "📄 run.py 内容预览（前20行）："
head -20 run.py
echo

# 3. 询问是否备份
read -p "是否创建备份？ (y/n): " backup_choice
if [ "$backup_choice" = "y" ]; then
    backup_name="run.py.backup_$(date +%Y%m%d_%H%M%S)"
    cp run.py "$backup_name"
    echo "✅ 已备份到: $backup_name"
fi

# 4. 删除文件
echo "🗑️  删除 run.py..."
rm run.py

# 5. 清理编译缓存
echo "🧹 清理编译缓存..."
find . -name "*.pyc" -delete 2>/dev/null
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null

# 6. 验证删除
if [ ! -f "run.py" ]; then
    echo "✅ run.py 已成功删除"
else
    echo "❌ 删除失败"
    exit 1
fi

# 7. 验证服务
echo -e "\n🔧 验证服务是否正常..."
docker-compose down >/dev/null 2>&1
docker-compose up -d >/dev/null 2>&1
sleep 8

if curl -s http://localhost:8000/health >/dev/null; then
    echo "✅ 服务运行正常"
else
    echo "❌ 服务可能有问题，请检查"
fi

echo -e "\n🎉 清理完成！"
