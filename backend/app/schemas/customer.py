from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field, ConfigDict

# 从 models 导入枚举类型
from app.models.customer import CustomerSource, CustomerType, CustomerStatus, Shop

class CustomerBase(BaseModel):
    """客户基础模型，包含共同的字段定义和验证规则"""
    shop: Annotated[
        Shop, 
        Field(description="店铺品牌（依/丽/末）")
    ]
    customer_id: Annotated[
        str, 
        Field(
            min_length=3,
            max_length=50,
            pattern="^[a-zA-Z0-9_-]+$",
            description="客户唯一标识，支持字母、数字、下划线和连字符"
        )
    ]
    source: Annotated[
        CustomerSource,
        Field(description="客户来源（自然流量/推荐）")
    ]
    customer_type: Annotated[
        CustomerType,
        Field(description="客户类型（新客户/老客户/号码变更）")
    ]
    demand: Annotated[
        int,
        Field(gt=0, lt=10000, description="客户需求量，范围1-9999")
    ]
    demand_description: Annotated[
        str | None,
        Field(
            default=None,
            max_length=500,
            description="需求描述（可选，最多500字）"
        )
    ]
    customer_status: Annotated[
        CustomerStatus,
        Field(description="客户状态（咨询中/样品/准备下单/死了）")
    ]
    expected_order_date: Annotated[
        datetime | None,
        Field(
            default=None,
            description="预期下单日期（可选）"
        )
    ]
    expected_order_amount: Annotated[
        float | None,
        Field(
            default=None,
            ge=0,
            lt=1000000,
            description="预期订单金额（可选，0-1000000）"
        )
    ]

class CustomerCreate(CustomerBase):
    """创建新客户时使用的数据模型"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "shop": "依",
                "customer_id": "CUST001",
                "source": "自然流量",
                "customer_type": "新客户",
                "demand": 100,
                "demand_description": "需要定制高端礼服，预算充足",
                "customer_status": "咨询中",
                "expected_order_date": "2024-01-20T00:00:00Z",
                "expected_order_amount": 1000.0
            }
        }
    )

class CustomerUpdate(BaseModel):
    """更新客户信息时使用的数据模型，所有字段都是可选的"""
    shop: Annotated[
        Shop | None,
        Field(default=None, description="店铺品牌（依/丽/末）")
    ] = None
    source: Annotated[
        CustomerSource | None,
        Field(default=None, description="客户来源（自然流量/推荐）")
    ] = None
    customer_type: Annotated[
        CustomerType | None,
        Field(default=None, description="客户类型（新客户/老客户/号码变更）")
    ] = None
    demand: Annotated[
        int | None,
        Field(default=None, gt=0, lt=10000, description="客户需求量，范围1-9999")
    ] = None
    demand_description: Annotated[
        str | None,
        Field(default=None, max_length=500, description="需求描述（可选，最多500字）")
    ] = None
    customer_status: Annotated[
        CustomerStatus | None,
        Field(default=None, description="客户状态（咨询中/样品/准备下单/死了）")
    ] = None
    expected_order_date: Annotated[
        datetime | None,
        Field(default=None, description="预期下单日期（可选）")
    ] = None
    expected_order_amount: Annotated[
        float | None,
        Field(default=None, ge=0, lt=1000000, description="预期订单金额（可选，0-1000000）")
    ] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "customer_status": "样品",
                "demand": 200,
                "expected_order_amount": 2000.0
            }
        }
    )

class Customer(CustomerBase):
    """完整的客户数据模型，包含数据库自动生成的字段"""
    id: Annotated[
        int,
        Field(description="数据库自增ID")
    ]
    creation_date: Annotated[
        datetime,
        Field(description="记录创建时间")
    ]
    last_modified_date: Annotated[
        datetime,
        Field(description="最后修改时间")
    ]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "shop": "依",
                "customer_id": "CUST001",
                "source": "自然流量",
                "customer_type": "新客户",
                "demand": 100,
                "demand_description": "需要定制高端礼服，预算充足",
                "customer_status": "咨询中",
                "expected_order_date": "2024-01-20T00:00:00Z",
                "expected_order_amount": 1000.0,
                "creation_date": "2024-01-01T00:00:00Z",
                "last_modified_date": "2024-01-01T00:00:00Z"
            }
        }
    )