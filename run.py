from fastapi import FastAPI
import prometheus_client
import uvicorn

app = FastAPI()

# 创建一个简单的计数器
REQUEST_COUNT = prometheus_client.Counter(
    'http_requests_total', 
    'Total HTTP requests'
)

@app.get("/")
def read_root():
    REQUEST_COUNT.inc()
    return {"message": "Smart Customer Service is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "smart-customer-service"}

@app.get("/metrics")
def get_metrics():
    return prometheus_client.generate_latest()

if __name__ == "__main__":
    print("Starting Smart Customer Service...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
