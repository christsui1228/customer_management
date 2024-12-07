"""
API v1 版本路由
"""

from fastapi import APIRouter

router = APIRouter()

# 导入所有路由
from .customer import router as customer_router

# 注册路由
router.include_router(customer_router)
