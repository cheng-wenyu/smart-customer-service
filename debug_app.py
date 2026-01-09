import sys
import os
sys.path.insert(0, '.')

try:
    # 尝试导入你的应用
    from src.api_service_final import app
    print("✅ 成功导入应用")
    
    # 打印所有已注册的路由
    print("\n=== 已注册的路由列表 ===")
    found_chat = False
    for route in app.routes:
        methods = list(route.methods) if route.methods else ["WS"]
        path = getattr(route, "path", "N/A")
        print(f"{methods}: {path}")
        if path == "/chat":
            found_chat = True
    
    if not found_chat:
        print("\n❌ 致命问题：/chat 路由 **没有** 在路由列表中！")
        print("可能的原因：")
        print("1. 路由定义的代码块因为缩进或格式问题，没有被执行。")
        print("2. 路由定义在某个条件判断（如 if __name__ ...）内部，导致没有被加载。")
        print("3. 文件中仍有其他语法或导入错误，导致部分代码未运行。")
    else:
        print("\n✅ /chat 路由已成功注册！问题可能出在别处。")

except Exception as e:
    print(f"\n❌ 导入应用时发生错误：{type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
