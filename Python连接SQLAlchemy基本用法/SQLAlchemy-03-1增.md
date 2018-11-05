# Table（表）类方式 - Insert
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
4. ## Insert
    ```python
    # 构造查询表达式（带有值）
    ins = tb_user.insert().values(username='ruirui', password='123456')
    print(str(ins))
    # 查看参数
    print(ins.compile().params)
    # 查看SQL
    print(ins.compile().string)

    # 创建连接
    conn = engine.connect()

    # 执行insert操作
    result = conn.execute(ins)
    # 如果是insert操作
    if result.is_insert:
        # 获取新添加的记录的主键
        print(result.inserted_primary_key)
    
    # 构造查询表达式（不带值）
    ins = tb_user.insert()
    print(str(ins))

    # 插入单条数据
    result = conn.execute(ins, username='aaron', password='hillel')

    # 插入多条数据
    data = [
        {'username': 'swartz', 'password' : '1234567'},
        {'username': 'gates', 'password' : '3456789'},
        {'username': 'bill', 'password' : '111222333'}
    ]
    result = conn.execute(ins, data)
    # 显示新增的条数
    print(result.rowcount)

    # 关闭连接
    conn.close()
   ```
5.  ## 销毁引擎
    ```python
    engine.dispose()
    ```