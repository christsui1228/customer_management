"""
客户 API 测试
"""
import pytest
from httpx import AsyncClient
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.main import app
from app.models.customer import Customer, CustomerSource, CustomerType, CustomerStatus, Shop

@pytest.mark.asyncio
async def test_create_customer():
    """测试创建客户"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        customer_data = {
            "shop": "依",
            "customer_id": "TEST001",
            "source": "自然流量",
            "customer_type": "新客户",
            "demand": 100,
            "demand_description": "测试客户",
            "customer_status": "咨询中"
        }
        response = await client.post(
            f"{settings.API_V1_STR}/customers/",
            json=customer_data
        )
        assert response.status_code == 201
        data = response.json()
        assert data["customer_id"] == "TEST001"
        assert data["shop"] == "依"

@pytest.mark.asyncio
async def test_read_customer():
    """测试读取客户"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            f"{settings.API_V1_STR}/customers/TEST001"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["customer_id"] == "TEST001"

@pytest.mark.asyncio
async def test_update_customer():
    """测试更新客户"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        update_data = {
            "customer_status": "样品",
            "demand": 200
        }
        response = await client.put(
            f"{settings.API_V1_STR}/customers/TEST001",
            json=update_data
        )
        assert response.status_code == 200
        data = response.json()
        assert data["customer_status"] == "样品"
        assert data["demand"] == 200

@pytest.mark.asyncio
async def test_delete_customer():
    """测试删除客户"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.delete(
            f"{settings.API_V1_STR}/customers/TEST001"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["detail"] == "客户删除成功"
