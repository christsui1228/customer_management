# 不使用 * 的情况
def update_user(name: str, age: int, email: str):
    print(f"更新用户：{name}, 年龄：{age}, 邮箱：{email}")

# 使用 * 的情况
def update_user_safe(*, name: str, age: int, email: str):
    print(f"更新用户：{name}, 年龄：{age}, 邮箱：{email}")

# 不使用 * 的函数可以这样调用
update_user("张三", 25, "zhangsan@example.com")  # 正常工作
update_user("zhang@example.com", 25, "张三")     # 工作但参数顺序错了！

# 使用 * 的函数必须这样调用
update_user_safe(name="张三", age=25, email="zhangsan@example.com")  # 正常工作
# update_user_safe("张三", 25, "zhangsan@example.com")  # ❌ 这样会报错！

# 在实际项目中的应用
async def create_customer(
    *,  # 强制使用关键字参数
    db: AsyncSession,
    name: str,
    email: str
) -> dict[str, str]:
    """
    创建客户的函数
    必须这样调用：
    await create_customer(
        db=db_session,
        name="张三",
        email="zhangsan@example.com"
    )
    """
    return {"status": "success", "message": f"创建客户：{name}"}
