# test_docker_service.py
import requests
import time
import json

def test_rag_service():
    """测试Docker中的RAG服务"""
    # 通常RAG服务运行在8000端口，但请根据实际情况调整
    base_url = "http://localhost:8000"
    
    test_endpoints = [
        "/",                     # 根路径
        "/docs",                 # API文档（如果是FastAPI）
        "/health",               # 健康检查
        "/query",                # 查询端点
        "/ask",                  # 另一个可能的端点
        "/api/query",            # API查询端点
    ]
    
    print("测试Docker中的RAG服务...")
    
    # 先测试根路径
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"根路径 ({base_url}/): 状态码 {response.status_code}")
        if response.status_code == 200:
            print(f"响应: {response.text[:100]}...")
    except requests.exceptions.RequestException as e:
        print(f"根路径连接失败: {e}")
        # 尝试其他端口
        ports_to_try = [8000, 8001, 8080, 80]
        for port in ports_to_try:
            try:
                url = f"http://localhost:{port}/"
                response = requests.get(url, timeout=2)
                print(f"尝试端口 {port}: 状态码 {response.status_code}")
                if response.status_code == 200:
                    base_url = f"http://localhost:{port}"
                    print(f"✓ 发现服务在 {base_url}")
                    break
            except:
                continue
    
    # 测试可能的API端点
    endpoints_to_test = ["/query", "/ask", "/api/query", "/chat"]
    test_query = {"query": "什么是机器学习？"}
    
    for endpoint in endpoints_to_test:
        try:
            print(f"\n测试端点 {endpoint}...")
            start_time = time.time()
            response = requests.post(
                f"{base_url}{endpoint}",
                json=test_query,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            elapsed = time.time() - start_time
            
            print(f"状态码: {response.status_code}")
            print(f"响应时间: {elapsed:.2f}秒")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✓ API端点 {endpoint} 工作正常！")
                print(f"响应类型: {type(result)}")
                print(f"响应内容: {json.dumps(result, indent=2, ensure_ascii=False)[:200]}...")
                return True, base_url, endpoint
            else:
                print(f"响应文本: {response.text[:200]}")
                
        except requests.exceptions.JSONDecodeError:
            print(f"响应不是JSON格式: {response.text[:200]}")
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
    
    return False, base_url, None

def test_prometheus():
    """测试Prometheus监控"""
    print("\n测试Prometheus监控...")
    try:
        response = requests.get("http://localhost:9090", timeout=5)
        print(f"Prometheus状态: {response.status_code}")
        return response.status_code == 200
    except:
        print("Prometheus不可达")
        return False

def test_grafana():
    """测试Grafana监控面板"""
    print("\n测试Grafana监控...")
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        print(f"Grafana状态: {response.status_code}")
        return response.status_code == 200
    except:
        print("Grafana不可达")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Docker服务测试")
    print("=" * 60)
    
    # 测试RAG服务
    rag_success, base_url, endpoint = test_rag_service()
    
    # 测试监控服务
    prometheus_success = test_prometheus()
    grafana_success = test_grafana()
    
    print("\n" + "=" * 60)
    print("测试结果汇总:")
    print(f"RAG服务: {'✓ 运行正常' if rag_success else '✗ 有问题'}")
    if rag_success:
        print(f"  API地址: {base_url}{endpoint}")
    print(f"Prometheus监控: {'✓ 运行正常' if prometheus_success else '✗ 不可达'}")
    print(f"Grafana面板: {'✓ 运行正常' if grafana_success else '✗ 不可达'}")
    print("=" * 60)
