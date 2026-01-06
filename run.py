from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Development with Hot Reload"}

@app.get("/health")
def health():
    return {"status": "healthy"}

# 导出app实例，用于uvicorn
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)

@app.get("/test-hot-reload")
def test_hot_reload():
    import time
    return {
        "message": "热重载测试成功！",
        "timestamp": time.time(),
        "environment": "development"
    }
