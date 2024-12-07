from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_db
from app.schemas.customer import CustomerCreate, CustomerUpdate, Customer
from app.crud.customer import create_customer, get_customer, get_customers, update_customer, delete_customer
from app.models.customer import Customer as CustomerModel  # 导入模型而不是 schema

# 创建路由器，设置URL前缀和API标签
router = APIRouter(
    prefix="/customers",
    tags=["customers"],
    responses={404: {"description": "找不到客户"}},
)

@router.post("/", 
            response_model=Customer, 
            status_code=201,
            summary="创建新客户",
            response_description="创建的客户信息")
async def create_new_customer(
    *,  # * 后的所有参数必须使用关键字参数
    db: AsyncSession = Depends(get_db),  # 数据库会话依赖注入
    customer: CustomerCreate  # 客户创建模型，包含所有必要字段
) -> Customer:
    """
    创建新客户，需要提供以下信息：
    - **shop**: 店铺品牌（依/丽/末）
    - **customer_id**: 客户唯一标识
    - **source**: 客户来源
    - **customer_type**: 客户类型
    - **demand**: 需求量
    - **customer_status**: 客户状态
    """
    return await create_customer(db=db, customer_create=customer)

@router.get("/{customer_id}", 
           response_model=Customer,
           summary="获取指定客户",
           response_description="客户详细信息")
async def read_customer(
    *,  # * 后的所有参数必须使用关键字参数
    db: AsyncSession = Depends(get_db),  # 数据库会话依赖注入
    customer_id: str  # 要查询的客户ID
) -> Customer:
    """
    根据客户ID获取客户详细信息
    """
    customer = await get_customer(db=db, customer_id=customer_id)
    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="客户未找到"
        )
    return customer

@router.get("/", 
           response_model=list[Customer],
           summary="获取客户列表",
           response_description="客户列表")
async def read_customers(
    *,  # * 后的所有参数必须使用关键字参数
    db: AsyncSession = Depends(get_db),  # 数据库会话依赖注入
    skip: int = Query(default=0, ge=0, description="跳过的记录数"),  # 分页参数：跳过记录数
    limit: int = Query(default=100, ge=1, le=1000, description="返回的最大记录数")  # 分页参数：每页记录数
) -> list[Customer]:
    """
    获取客户列表，支持分页：
    - **skip**: 跳过前面的记录数
    - **limit**: 返回的最大记录数
    """
    customers = await get_customers(db=db, skip=skip, limit=limit)
    return customers

@router.put("/{customer_id}", 
           response_model=Customer,
           summary="更新客户信息",
           response_description="更新后的客户信息")
async def update_existing_customer(
    *,  # * 后的所有参数必须使用关键字参数
    db: AsyncSession = Depends(get_db),  # 数据库会话依赖注入
    customer_id: str,  # 要更新的客户ID
    customer: CustomerUpdate  # 客户更新模型，所有字段都是可选的
) -> Customer:
    """
    更新指定客户的信息，所有字段都是可选的
    """
    updated_customer = await update_customer(db=db, customer_id=customer_id, customer_update=customer)
    if updated_customer is None:
        raise HTTPException(
            status_code=404,
            detail="客户未找到"
        )
    return updated_customer

@router.put("/id/{id}", 
           response_model=Customer,
           summary="通过ID更新客户信息",
           response_description="更新后的客户信息")
async def update_customer_by_id(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
    customer: CustomerUpdate
) -> Customer:
    """
    通过数据库ID更新指定客户的信息，所有字段都是可选的
    """
    # 先查找客户
    query = select(CustomerModel).where(CustomerModel.id == id)
    result = await db.execute(query)
    db_customer = result.scalar_one_or_none()
    
    if not db_customer:
        raise HTTPException(
            status_code=404,
            detail="客户未找到"
        )
    
    # 更新客户信息
    customer_data = customer.dict(exclude_unset=True)
    for key, value in customer_data.items():
        setattr(db_customer, key, value)
    
    await db.commit()
    await db.refresh(db_customer)
    return db_customer

@router.delete("/{customer_id}",
             status_code=204,
             summary="删除客户",
             response_description="成功删除")
async def remove_customer(
    *,  # * 后的所有参数必须使用关键字参数
    db: AsyncSession = Depends(get_db),  # 数据库会话依赖注入
    customer_id: str  # 要删除的客户ID
):
    """
    删除指定的客户
    """
    success = await delete_customer(db=db, customer_id=customer_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="客户未找到"
        )