# Table（表）类方式 - Select
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
4. ## Select
    ```python
    # 构造查询表达式（无条件）
    sel = tb_user.select()
    print(str(sel))

    # 构造查询表达式（带条件: 8 <= id <= 9）
    sel = tb_user.select().where(
        tb_user.columns.id.between(8, 9)
    )
    print(str(sel))

    # 创建连接
    conn = engine.connect()

    # 执行select操作
    result = conn.execute(sel)

    # 是否返回了结果
    if result.returns_rows:
        # 取一条
        print(result.fetchone())
        print(result.closed)
        # 取N条
        N = 2
        print(result.fetchmany(N))
        # 取剩余的所有条
        print(result.fetchall())

        # 关闭结果游标
        result.close()
    
    # 执行select操作
    result = conn.execute(sel)

    # 取第一条(first()方法自动关闭游标)
    print(result.first())
    print(result.closed)

    # 关闭连接
    conn.close()
   ```
5.  ## 销毁引擎
    ```python
    engine.dispose()
    ```