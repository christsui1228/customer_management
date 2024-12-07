from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from app.api.v1.customer import router as customer_router
from app.core.database import engine
from app.models.customer import Customer  # 导入 Customer 模型

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用程序生命周期管理
    启动时创建数据库表
    关闭时释放数据库连接
    """
    print("应用程序启动...")
    async with engine.begin() as conn:
        # 确保所有模型都被导入后再创建表
        # SQLModel.metadata 会包含所有已导入的模型定义
        print("创建数据库表...")
        await conn.run_sync(SQLModel.metadata.create_all)
        print("数据库表创建完成")
    
    yield  # 应用运行期间
    
    print("应用程序关闭...")
    await engine.dispose()

# 创建 FastAPI 应用实例
app = FastAPI(
    title="客户管理系统",
    description="使用 FastAPI 和 SQLModel 构建的客户管理系统API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",  # Swagger UI 路径
    redoc_url="/redoc",  # ReDoc 路径
    openapi_url="/openapi.json"  # OpenAPI 模式路径
)

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:9527", "http://localhost:5173","http://localhost:5174", "http://127.0.0.1:5173","http://127.0.0.1:9527"],  # 允许的前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(customer_router, prefix="/api/v1")

@app.get("/", tags=["root"])
async def root() -> dict[str, str]:
    """
    根路径，返回简单的欢迎信息
    """
    return {
        "message": "欢迎使用客户管理系统API",
        "docs": "访问 /docs 查看完整API文档"
    }

if __name__ == "__main__":
    import uvicorn
    
    # 使用 uvicorn 启动应用
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 开发模式下启用热重载
        workers=1  # 工作进程数
    )
