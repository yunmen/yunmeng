# Table（表）类方式 - Update
```python
# 导入引擎创建函数
from sqlalchemy import create_engine
# 导入语句处理函数
from sqlalchemy.sql.expression import text

# 导入元数据、表类
from sqlalchemy import MetaData, Table
# 导入数据类型
from sqlalchemy import Integer, String, Text, DateTime
# 导入列类和关联
from sqlalchemy import Column, ForeignKey
```

1. ## 创建引擎
    ```python
    uri = 'mysql+pymysql://root:root@127.0.0.1:3306/user_system?charset=utf8'
    # create_engine()有一个关键字参数echo, 表示是否输出debug信息，默认为False
    engine = create_engine(uri, echo=True)
    ```
2. ## 构建元数据
    ```python
    # 元数据: 主要是指数据库表结构、关联等信息
    # 实例化MetaData(从引擎读取元数据)
    meta = MetaData(bind=engine)
    ```
3. ## 获取表
    ```python
    tb_user = Table('tb_user', meta, autoload=True, autoload_with=engine)
    ```
4. ## Update
    ```python
    # 构造更新表达式（无条件）
    upt = tb_user.update()
    print(str(upt))

    # 构造更新表达式（带条件: 8 <= id <= 9）
    upt_nd = tb_user.update().where(
        tb_user.columns.id.between(8, 9)
    )
    print(str(upt_nd))

    # 构造更新表达式（带值）
    upt = tb_user.update().values(username='新来的')
    print(str(upt))
    upt = tb_user.update().values(username='Python', password='py666789')
    print(str(upt))

    # 构造更新表达式（带条件和值）(可以用多个where)
    new_data = {
        'username': 'new数据',
        'password': '123456'
    }
    upt = tb_user.update().where(
        tb_user.columns['id'] > 10
    ).values(**new_data)
    print(str(upt))

    # 创建连接
    conn = engine.connect()

    # 执行update操作（对于带值的Update）
    result = conn.execute(upt)

    # 执行update操作（没有带值的Update）
    result = conn.execute(upt_nd, password='6ge654321')

    # 显示更新的条数
    print(result.rowcount)

    # 关闭连接
    conn.close()
   ```
5.  ## 销毁引擎
    ```python
    engine.dispose()
    ```