from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate

async def create_customer(
    db: AsyncSession,
    customer_create: CustomerCreate) -> Customer:
    """
    创建客户
    """
    db_customer = Customer.from_orm(customer_create)
    db.add(db_customer)
    await db.commit()
    await db.refresh(db_customer)
    return db_customer

async def get_customer(
    db: AsyncSession,
    customer_id: str) -> Optional[Customer]:
    """
    获取客户
    """
    query = select(Customer).where(Customer.customer_id == customer_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_customers(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100) -> List[Customer]:
    """
    获取客户列表
    """
    query = select(Customer).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def update_customer(
    db: AsyncSession,
    customer_id: str,
    customer_update: CustomerUpdate) -> Optional[Customer]:
    """
    更新客户
    """
    query = select(Customer).where(Customer.customer_id == customer_id)
    result = await db.execute(query)
    db_customer = result.scalar_one_or_none()
    
    if not db_customer:
        return None
    
    customer_data = customer_update.dict(exclude_unset=True)
    for key, value in customer_data.items():
        setattr(db_customer, key, value)
    
    await db.commit()
    await db.refresh(db_customer)
    return db_customer

async def delete_customer(
    db: AsyncSession,
    customer_id: str) -> bool:
    """
    删除客户
    """
    query = select(Customer).where(Customer.customer_id == customer_id)
    result = await db.execute(query)
    db_customer = result.scalar_one_or_none()
    
    if not db_customer:
        return False
    
    await db.delete(db_customer)
    await db.commit()
    return True
