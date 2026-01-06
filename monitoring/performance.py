import time
import psutil
from prometheus_client import Counter, Histogram, Gauge, Summary
import GPUtil
import json
from datetime import datetime
import os

# Prometheus指标
REQUEST_COUNT = Counter('rag_requests_total', 'Total RAG requests')
REQUEST_LATENCY = Histogram('rag_request_latency_seconds', 'RAG request latency', buckets=[0.1, 0.5, 1.0, 2.0, 5.0])
RESPONSE_LENGTH = Histogram('rag_response_length_chars', 'Response length in characters', buckets=[100, 500, 1000, 2000, 5000])
GPU_MEMORY_USAGE = Gauge('gpu_memory_usage_bytes', 'GPU memory usage in bytes')
GPU_UTILIZATION = Gauge('gpu_utilization_percent', 'GPU utilization percentage')
ERROR_COUNT = Counter('rag_errors_total', 'Total RAG errors')

class PerformanceMonitor:
    def __init__(self, log_dir="logs/monitoring"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(log_dir, "performance.log")
        
    def record_request_start(self):
        """记录请求开始，返回请求ID"""
        return {
            'request_id': str(time.time()),
            'start_time': time.time(),
            'start_cpu': psutil.cpu_percent(percpu=False),
            'start_memory': psutil.virtual_memory().percent
        }
    
    def record_request_end(self, request_data, query, response_text="", error=False):
        """记录请求结束"""
        end_time = time.time()
        processing_time = end_time - request_data['start_time']
        
        # 更新Prometheus指标
        REQUEST_COUNT.inc()
        REQUEST_LATENCY.observe(processing_time)
        RESPONSE_LENGTH.observe(len(response_text))
        
        if error:
            ERROR_COUNT.inc()
        
        # 记录详细日志
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'request_id': request_data['request_id'],
            'query': query[:200],  # 限制长度
            'response_preview': response_text[:200] if response_text else "",
            'processing_time_seconds': processing_time,
            'response_length': len(response_text),
            'cpu_usage_percent': psutil.cpu_percent(percpu=False),
            'memory_usage_percent': psutil.virtual_memory().percent,
            'error': error,
            'gpu_metrics': self._get_gpu_metrics()
        }
        
        # 写入日志文件
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(metrics, ensure_ascii=False) + '\n')
        
        return metrics
    
    def _get_gpu_metrics(self):
        """获取GPU指标"""
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                GPU_MEMORY_USAGE.set(gpus[0].memoryUsed * 1024 * 1024)  # MB to bytes
                GPU_UTILIZATION.set(gpus[0].load * 100)
                return {
                    'gpu_utilization': gpus[0].load * 100,
                    'gpu_memory_used_mb': gpus[0].memoryUsed,
                    'gpu_memory_total_mb': gpus[0].memoryTotal
                }
        except Exception as e:
            # GPU不可用或无GPU
            pass
        return None
    
    def generate_summary(self, last_n=100):
        """生成性能摘要"""
        if not os.path.exists(self.log_file):
            return {"error": "No performance data available"}
        
        try:
            with open(self.log_file, 'r') as f:
                lines = f.readlines()[-last_n:]
            
            metrics_list = [json.loads(line) for line in lines if line.strip()]
            
            if not metrics_list:
                return {"message": "No metrics collected yet"}
            
            # 计算统计信息
            processing_times = [m['processing_time_seconds'] for m in metrics_list]
            response_lengths = [m['response_length'] for m in metrics_list]
            
            return {
                'total_requests': len(metrics_list),
                'error_rate': sum(1 for m in metrics_list if m.get('error')) / len(metrics_list),
                'avg_processing_time': sum(processing_times) / len(processing_times),
                'max_processing_time': max(processing_times),
                'min_processing_time': min(processing_times),
                'avg_response_length': sum(response_lengths) / len(response_lengths),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e)}
