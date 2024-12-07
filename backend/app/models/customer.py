from datetime import datetime, timezone
from enum import Enum as PyEnum
from sqlmodel import Field, SQLModel
from sqlalchemy import DateTime

class CustomerSource(str, PyEnum):
    NATURAL_FLOW = "NATURAL_FLOW"
    RECOMMENDED = "RECOMMENDED"

class CustomerType(str, PyEnum):
    NEW = "NEW"
    OLD = "OLD"
    OLD_CHANGED_ID = "OLD_CHANGED_ID"

class CustomerStatus(str, PyEnum):
    CONSULTING = "CONSULTING"
    SAMPLE = "SAMPLE"
    PREPARING_ORDER = "PREPARING_ORDER"
    DEAD = "DEAD"

class Shop(str, PyEnum):
    YI = "YI"
    LI = "LI"
    MO = "MO"

class Customer(SQLModel, table=True):
    __tablename__ = "customer_management"
    id: int | None = Field(default=None, primary_key=True, index=True)
    shop: Shop= Field(..., sa_column_kwargs={"nullable": False})
    customer_id: str = Field(..., max_length=50, unique=True, sa_column_kwargs={"nullable": False})
    source: CustomerSource = Field(..., sa_column_kwargs={"nullable": False})
    customer_type: CustomerType = Field(..., sa_column_kwargs={"nullable": False})
    demand: int = Field(..., sa_column_kwargs={"nullable": False})
    demand_description: str | None = Field(default=None)
    customer_status: CustomerStatus = Field(..., sa_column_kwargs={"nullable": False})
    expected_order_date: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True)
    )
    expected_order_amount: float | None = Field(default=None)
    last_modified_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)}
    )
    creation_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True)
    )