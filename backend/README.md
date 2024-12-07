# 客户管理系统后端

基于 FastAPI 和 SQLModel 构建的现代化客户管理系统后端。

## 技术栈

- Python 3.12
- FastAPI
- SQLModel (基于 SQLAlchemy 2.0)
- Pydantic v2
- PDM (Python 依赖管理)
- Pytest (测试框架)

## 项目结构

```
backend/
├── app/                    # 应用主目录
│   ├── api/               # API 路由
│   │   └── v1/           # API v1 版本
│   ├── core/             # 核心配置
│   ├── crud/             # 数据库操作
│   ├── models/           # SQLModel 模型
│   └── schemas/          # Pydantic 模型
├── tests/                 # 测试目录
└── main.py               # 应用入口
```

## 开发环境设置

1. 安装 Python 3.12
2. 安装 PDM：`pip install pdm`
3. 安装依赖：`pdm install`
4. 复制 `.env.example` 到 `.env` 并配置环境变量
5. 运行开发服务器：`pdm run uvicorn main:app --reload`

## API 文档

启动服务器后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 测试

运行测试：
```bash
pdm run pytest
```

## 主要功能

- 客户信息管理 (CRUD 操作)
- 异步数据库操作
- 类型安全的数据验证
- 自动生成的 API 文档
- 完整的测试覆盖

## 开发规范

- 使用 Python 3.12 类型注解
- 遵循 PEP 8 编码规范
- 所有函数和类都要有文档字符串
- 使用异步编程模型
- 保持代码简洁和模块化
