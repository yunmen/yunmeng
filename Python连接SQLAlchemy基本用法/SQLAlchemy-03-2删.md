# Table（表）类方式 - Delete
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
4. ## Delete
    ```python
    # 构造删除表达式（无条件）
    dlt = tb_user.delete()
    print(str(dlt))

    # 构造删除表达式（带条件: id >= 10）
    dlt = tb_user.delete().where(
        tb_user.columns['id'] >= 10
    )
    print(str(dlt))

    # 构造删除表达式（带条件: password以1开头）
    dlt = tb_user.delete().where(
        tb_user.columns['password'].startswith('1')
    )
    print(str(dlt))

    # 构造删除表达式（带多个条件: password包含3但是不包含9,且id<10）
    dlt = tb_user.delete().where(
        tb_user.columns['password'].like('%3%')
    ).where(
        tb_user.columns['password'].notlike('%9%')
    ).where(
        tb_user.columns['id'] < 10
    )
    print(str(dlt))

    # 创建连接
    conn = engine.connect()

    # 执行delete操作
    result = conn.execute(dlt)

    # 显示删除的条数
    print(result.rowcount)

    # 关闭连接
    conn.close()
   ```
5.  ## 显示SQL语句
    ```python
    def structure_sql(sql_str_or_stmt, dialect_obj=None, sql_params=None, return_obj=False):
        '''
        构造SQL语句
        参数:
            sql_str_or_stmt: 原始（Raw）SQL字符串或Statement（Select、Insert、Update、Delete）对象
            dialect_obj: 数据库专用术语对象
            sql_params: 参数
            return_obj: 是否返回编译对象（默认否，返回字符串）
        refer: https://stackoverflow.com/questions/5631078/sqlalchemy-print-the-actual-query#answer-45551136
        '''
        stmt = sql_str_or_stmt
        # 如果是原始字符串，则包装成 Statement 对象
        if isinstance(stmt, str):
            stmt = text(stmt)
        
        if bool(sql_params):
            # Insert、Delete、Update和Select本身带有参数，无需额外参数绑定，没有bindparams()方法
            if hasattr(stmt, 'bindparams'):
                stmt = stmt.bindparams(**sql_params)

        # 获取数据库专业术语
        if dialect_obj is None:
            # 如果没有指定，则从语句绑定的引擎中获取
            if bool(stmt.bind):
                dialect_obj = stmt.bind.dialect
            else:
                # 如果没有指定，也没有绑定引擎，则抛出错误
                raise ValueError('参数 [dialect_obj] 未指定')

        # 编译语句
        full_sql = stmt.compile(
            dialect=dialect_obj,
            compile_kwargs={"literal_binds": True}
        )
        return full_sql if return_obj else full_sql.string
    ```
6.  ## 销毁引擎
    ```python
    engine.dispose()
    ```