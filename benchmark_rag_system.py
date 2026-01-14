#!/usr/bin/env python3
# benchmark_rag_system.py - RAG系统性能基准测试工具

import time
import logging
import json
import asyncio
import aiohttp
from datetime import datetime
from typing import List, Dict, Any
import statistics

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RAGBenchmark:
    """RAG系统性能基准测试类"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = []
    
    async def test_single_query(self, session: aiohttp.ClientSession, 
                               query: str, query_id: int = None) -> Dict[str, Any]:
        """测试单个查询"""
        try:
            # 开始计时
            start_time = time.time()
            
            # 发送请求到RAG API
            async with session.post(
                f"{self.base_url}/ask",
                json={"question": query},
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                end_time = time.time()
                
                if response.status == 200:
                    data = await response.json()
                    elapsed_time = end_time - start_time
                    
                    result = {
                        "query": query,
                        "query_id": query_id,
                        "success": True,
                        "response_time": elapsed_time,
                        "response": data.get("answer", ""),
                        "context_length": len(data.get("context", "")),
                        "timestamp": datetime.now().isoformat(),
                        "status_code": response.status
                    }
                    logger.info(f"✓ 查询{query_id if query_id else ''}: '{query[:30]}...' - {elapsed_time:.3f}秒")
                    return result
                else:
                    error_text = await response.text()
                    result = {
                        "query": query,
                        "query_id": query_id,
                        "success": False,
                        "response_time": time.time() - start_time,
                        "error": f"HTTP {response.status}: {error_text}",
                        "timestamp": datetime.now().isoformat(),
                        "status_code": response.status
                    }
                    logger.error(f"✗ 查询{query_id if query_id else ''}: '{query[:30]}...' 失败 - {response.status}")
                    return result
                    
        except asyncio.TimeoutError:
            result = {
                "query": query,
                "query_id": query_id,
                "success": False,
                "response_time": 30,
                "error": "请求超时 (30秒)",
                "timestamp": datetime.now().isoformat(),
                "status_code": 408
            }
            logger.error(f"✗ 查询{query_id if query_id else ''}: '{query[:30]}...' 超时")
            return result
            
        except Exception as e:
            result = {
                "query": query,
                "query_id": query_id,
                "success": False,
                "response_time": time.time() - start_time,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "status_code": 500
            }
            logger.error(f"✗ 查询{query_id if query_id else ''}: '{query[:30]}...' 异常: {e}")
            return result
    
    async def run_concurrent_test(self, queries: List[str], 
                                 concurrent_requests: int = 3) -> List[Dict[str, Any]]:
        """运行并发测试"""
        logger.info(f"开始并发测试，并发数: {concurrent_requests}")
        
        # 创建连接池
        connector = aiohttp.TCPConnector(limit=concurrent_requests)
        
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = []
            for i, query in enumerate(queries):
                task = asyncio.create_task(
                    self.test_single_query(session, query, i + 1)
                )
                tasks.append(task)
            
            # 等待所有任务完成
            results = await asyncio.gather(*tasks)
            self.results = results
            return results
    
    def generate_report(self, output_file: str = "benchmark_report.json") -> Dict[str, Any]:
        """生成性能测试报告"""
        if not self.results:
            logger.warning("没有测试结果")
            return {}
        
        # 分离成功和失败的结果
        successful_results = [r for r in self.results if r["success"]]
        failed_results = [r for r in self.results if not r["success"]]
        
        if successful_results:
            response_times = [r["response_time"] for r in successful_results]
            context_lengths = [r["context_length"] for r in successful_results]
            
            report = {
                "test_summary": {
                    "total_queries": len(self.results),
                    "successful_queries": len(successful_results),
                    "failed_queries": len(failed_results),
                    "success_rate": len(successful_results) / len(self.results) * 100,
                    "test_timestamp": datetime.now().isoformat(),
                    "average_response_time": statistics.mean(response_times),
                    "median_response_time": statistics.median(response_times),
                    "min_response_time": min(response_times),
                    "max_response_time": max(response_times),
                    "response_time_stddev": statistics.stdev(response_times) if len(response_times) > 1 else 0,
                    "average_context_length": statistics.mean(context_lengths) if context_lengths else 0,
                    "total_test_duration": sum(response_times)
                },
                "performance_metrics": {
                    "queries_per_second": len(successful_results) / sum(response_times) if sum(response_times) > 0 else 0,
                    "average_latency": statistics.mean(response_times),
                    "p95_response_time": sorted(response_times)[int(len(response_times) * 0.95)] if response_times else 0,
                    "p99_response_time": sorted(response_times)[int(len(response_times) * 0.99)] if response_times else 0
                },
                "detailed_results": self.results,
                "failed_queries": failed_results
            }
        else:
            report = {
                "test_summary": {
                    "total_queries": len(self.results),
                    "successful_queries": 0,
                    "failed_queries": len(failed_results),
                    "success_rate": 0,
                    "test_timestamp": datetime.now().isoformat(),
                    "error": "所有查询都失败了"
                },
                "detailed_results": self.results
            }
        
        # 保存报告到文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        # 打印报告摘要
        self.print_report_summary(report)
        
        return report
    
    def print_report_summary(self, report: Dict[str, Any]):
        """打印报告摘要"""
        print("\n" + "="*80)
        print("RAG系统性能测试报告")
        print("="*80)
        
        if "test_summary" in report:
            summary = report["test_summary"]
            print(f"\n📊 测试概要:")
            print(f"  测试时间: {summary['test_timestamp']}")
            print(f"  总查询数: {summary['total_queries']}")
            print(f"  成功查询: {summary['successful_queries']}")
            print(f"  失败查询: {summary['failed_queries']}")
            print(f"  成功率: {summary['success_rate']:.1f}%")
            
            if summary['successful_queries'] > 0:
                print(f"\n⏱️ 响应时间统计:")
                print(f"  平均响应时间: {summary['average_response_time']:.3f} 秒")
                print(f"  中位数响应时间: {summary['median_response_time']:.3f} 秒")
                print(f"  最小响应时间: {summary['min_response_time']:.3f} 秒")
                print(f"  最大响应时间: {summary['max_response_time']:.3f} 秒")
                print(f"  标准差: {summary['response_time_stddev']:.3f} 秒")
                
                if "performance_metrics" in report:
                    metrics = report["performance_metrics"]
                    print(f"\n🚀 性能指标:")
                    print(f"  查询/秒: {metrics['queries_per_second']:.2f}")
                    print(f"  P95响应时间: {metrics['p95_response_time']:.3f} 秒")
                    print(f"  P99响应时间: {metrics['p99_response_time']:.3f} 秒")
        
        print("\n" + "="*80)
    
    def load_test_queries(self) -> List[str]:
        """加载测试问题"""
        # 尝试从文件加载
        try:
            with open('test_questions.py', 'r', encoding='utf-8') as f:
                content = f.read()
                # 简单解析问题列表
                import re
                questions = re.findall(r'question\s*=\s*["\'](.*?)["\']', content)
                if questions:
                    return questions
        except:
            pass
        
        # 如果文件不存在或解析失败，使用默认问题
        default_queries = [
            "如何退货？",
            "你们的售后服务政策是什么？",
            "产品质量有问题怎么办？",
            "订单什么时候发货？",
            "支持哪些支付方式？",
            "运费怎么计算？",
            "可以开发票吗？",
            "商品有保修吗？",
            "如何联系客服？",
            "订单能修改吗？",
            "什么是机器学习？",
            "解释一下深度学习",
            "RAG是什么？",
            "什么是Transformer模型？",
            "如何训练一个神经网络？"
        ]
        return default_queries

async def main():
    """主函数"""
    print("\n🔍 RAG系统性能基准测试工具")
    print("="*60)
    
    # 获取测试配置
    try:
        import argparse
        parser = argparse.ArgumentParser(description='RAG系统性能测试')
        parser.add_argument('--url', default='http://localhost:8000', help='API服务地址')
        parser.add_argument('--concurrent', type=int, default=3, help='并发请求数')
        parser.add_argument('--queries', type=int, default=10, help='测试问题数量')
        parser.add_argument('--output', default='benchmark_report.json', help='输出文件')
        args = parser.parse_args()
    except:
        # 如果argparse不可用，使用默认值
        class Args:
            url = 'http://localhost:8000'
            concurrent = 3
            queries = 10
            output = 'benchmark_report.json'
        args = Args()
    
    # 创建测试器
    benchmark = RAGBenchmark(base_url=args.url)
    
    # 加载测试问题
    all_queries = benchmark.load_test_queries()
    test_queries = all_queries[:args.queries] if args.queries <= len(all_queries) else all_queries
    
    print(f"\n📋 测试配置:")
    print(f"  API地址: {args.url}")
    print(f"  并发数: {args.concurrent}")
    print(f"  测试问题数: {len(test_queries)}")
    print(f"  输出文件: {args.output}")
    
    print("\n📝 测试问题:")
    for i, query in enumerate(test_queries, 1):
        print(f"  {i:2d}. {query}")
    
    input("\n按 Enter 键开始测试...")
    
    # 运行测试
    print(f"\n🚀 开始性能测试...")
    print("-"*60)
    
    await benchmark.run_concurrent_test(test_queries, args.concurrent)
    
    # 生成报告
    print(f"\n📈 生成测试报告...")
    benchmark.generate_report(args.output)
    
    print(f"\n✅ 测试完成！详细报告已保存到: {args.output}")

if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())
