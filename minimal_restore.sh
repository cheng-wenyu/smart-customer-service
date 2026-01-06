#!/bin/bash
echo "=== 最小影响恢复方案 ==="
echo "只修复已知问题，不猜测历史"

# 1. 修复 vector_search.py 的 TabError（无论什么原因）
echo "1. 修复 vector_search.py 的缩进问题..."
if [ -f "src/vector_search.py" ]; then
    # 备份
    cp src/vector_search.py src/vector_search.py.backup.$(date +%H%M%S)
    # 修复制表符
    sed -i 's/\t/    /g' src/vector_search.py
    echo "  缩进已修复"
    
    # 验证语法
    if python -m py_compile src/vector_search.py 2>/dev/null; then
        echo "  ✅ 语法正确"
    else
        echo "  ⚠ 仍有语法问题，显示错误："
        python -m py_compile src/vector_search.py
    fi
fi

# 2. 删除我们明确知道是今晚新增的问题文件
echo -e "\n2. 清理明确的新增文件..."
PROBLEM_FILES=(
    "run.py"                    # 新创建的应用文件
    "src/feedback/"             # 反馈模块
    "config/sls_config.yaml"    # 阿里云配置
    "static/js/feedback.js"     # 反馈JS
    "fix_indent.py"             # 修复脚本
    "test_feedback_system.py"   # 测试脚本
)

for item in "${PROBLEM_FILES[@]}"; do
    if [ -e "$item" ]; then
        rm -rf "$item"
        echo "  删除: $item"
    fi
done

# 3. 恢复 docker-compose.yml 到已知可用状态
echo -e "\n3. 恢复 Docker 配置..."
if [ -f "docker-compose.yml.backup" ]; then
    cp docker-compose.yml.backup docker-compose.yml
    echo "  从备份恢复 docker-compose.yml"
elif [ -f "docker-compose.yml" ]; then
    # 检查内容
    if grep -q "5000:5000" docker-compose.yml; then
        echo "  ✅ docker-compose.yml 看起来正常"
    else
        echo "  ⚠  docker-compose.yml 可能需要检查"
    fi
fi

# 4. 让用户决定 chat.html 的处理
echo -e "\n4. 处理聊天界面..."
if [ -f "templates/chat.html" ]; then
    if grep -q "feedback-buttons" templates/chat.html; then
        echo "  发现反馈按钮，您想："
        echo "  1) 保留反馈按钮"
        echo "  2) 恢复原版界面"
        read -p "  选择 (1/2): " choice
        if [ "$choice" = "2" ]; then
            if [ -f "templates/chat.html.backup" ]; then
                cp templates/chat.html.backup templates/chat.html
                echo "  已恢复原版界面"
            else
                echo "  ⚠ 没有备份，无法恢复"
            fi
        else
            echo "  保留反馈按钮"
        fi
    else
        echo "  没有发现反馈按钮"
    fi
fi

# 5. 测试系统
echo -e "\n5. 测试系统..."
echo "尝试导入关键模块："
python -c "
import sys
sys.path.insert(0, '.')
try:
    import src.api_service
    print('✅ 可以导入 api_service')
except Exception as e:
    print(f'❌ 导入失败: {e}')
    import traceback
    traceback.print_exc()
"

echo -e "\n=== 恢复完成 ==="
echo "已修复已知问题，保留了其他所有修改"
echo "现在可以尝试启动系统"
echo "Python启动: python -m src.api_service"
echo "Docker启动: docker-compose up -d"
