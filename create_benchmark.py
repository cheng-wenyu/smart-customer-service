# create_benchmark.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import time
import logging
import asyncio

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def benchmark_rag_system():
    """测试RAG系统性能"""
    try:
        # 尝试导入你的RAG系统
        from src.api_service_final import process_query, rag_pipeline
        logger.info("成功导入RAG模块")
        
        # 测试问题
        test_queries = [
            "什么是机器学习？",
            "如何退货？",
            "你们的客服政策是什么？",
            "产品有问题怎么办？"
        ]
        
        results = []
        for query in test_queries:
            logger.info(f"\n{'='*50}")
            logger.info(f"测试查询: '{query}'")
            
            # 测量时间
            start_time = time.time()
            
            try:
                # 尝试不同的函数调用方式
                # 方式1：直接调用 process_query
                answer = process_query(query)
                # 方式2：或者使用 rag_pipeline(query)
                # answer = rag_pipeline(query)
                
                end_time = time.time()
                elapsed = end_time - start_time
                
                logger.info(f"✓ 查询处理成功")
                logger.info(f"  耗时: {elapsed:.3f}秒")
                logger.info(f"  答案长度: {len(answer) if answer else 0}字符")
                logger.info(f"  答案预览: {str(answer)[:100]}...")
                
                results.append({
                    "query": query,
                    "time": elapsed,
                    "answer_length": len(answer) if answer else 0
                })
                
            except Exception as e:
                logger.error(f"✗ 查询处理失败: {e}")
                continue
                
        # 汇总结果
        logger.info(f"\n{'='*50}")
        logger.info("性能测试汇总:")
        logger.info(f"总测试数: {len(test_queries)}")
        logger.info(f"成功数: {len(results)}")
        
        if results:
            avg_time = sum(r["time"] for r in results) / len(results)
            logger.info(f"平均处理时间: {avg_time:.3f}秒")
            logger.info(f"最短时间: {min(r['time'] for r in results):.3f}秒")
            logger.info(f"最长时间: {max(r['time'] for r in results):.3f}秒")
            
    except ImportError as e:
        logger.error(f"导入模块失败: {e}")
        logger.info("尝试其他导入方式...")
        
        # 尝试其他可能的模块
        modules_to_try = [
            "src.api_service",
            "src.llm_generator",
            "src.vector_search"
        ]
        
        for module_name in modules_to_try:
            try:
                module = __import__(module_name, fromlist=[''])
                logger.info(f"成功导入 {module_name}")
                # 列出模块中的函数
                functions = [attr for attr in dir(module) if not attr.startswith('_')]
                logger.info(f"可用函数/类: {functions[:10]}")
            except ImportError:
                continue

if __name__ == "__main__":
    # 运行异步测试
    asyncio.run(benchmark_rag_system())
