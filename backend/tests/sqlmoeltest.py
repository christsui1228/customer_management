from sqlmodel import field,session,SQLModel,create_engine,select


class Hero(SQLModel, table=True):
    id: int | None = field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = field(default=None)

