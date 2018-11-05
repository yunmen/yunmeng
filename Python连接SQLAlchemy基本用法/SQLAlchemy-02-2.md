# Table（表）类方式 - Table类和Column类
```python
from sqlalchemy import create_engine

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
    # 实例化MetaData(不绑定任何引擎，通用的关系型数据库支持)
    meta_new = MetaData()
    ```
3. ## Table构造方法
    > `Table(name, metadata[, *column_list][, **kwargs])`
    > ##### 参数说明：
    > - `name` 表名
    > - `metadata` 元数据对象
    > - `column_list` 是列(`Column`或其他继承自`SchemaItem`的对象)列表
    > - `kwargs`主要内容：
    >     + `schema`: (`None`)表的模式（一般默认是数据库名, 无需特别指定; Oracle中是`owner`, 当一个数据库由多个用户管理时，用户的默认数据库不是要连接的数据库时，需要指定此项）
    >     + `autoload`: (`False`)是否自动加载
    >     + `autoload_replace`: (`True`)是否自动用元数据中加载的列替换`column_list`中已经存在了的同名列
    >         * 为`True`时自动将`column_list`中已经存在了的列替换为从元数据中加载的同名列
    >         * 为`False`时会忽略元数据有，且`column_list`中已经存在了的列
    >     + `autoload_with`: 自动加载的引擎(`Engine`)或连接(`Connection`)对象
    >         * 为`None`时
    >             - `autoload`为`True`时, 会从传递的`metadata`中寻找引擎或连接对象
    >         * 不为`None`时
    >             - 当`autoload`不为`True`时, `autoload`会自动被修改为`True`
    >     + `comment`: 注释
    >     + `extend_existing`: (`False`)当表已经存在于元数据中时，如果元数据中存在与`column_list`中的列同名的列，`column_list`中同名的列会替换掉元数据中已经有的列
    >     + `keep_existing`: (`False`)当表已经存在于元数据中时，如果元数据中存在与`column_list`中的列同名的列，`column_list`中同名的列会被忽略
    >     + `include_columns`：(`None`)从元数据中只需加载的表的列名列表
    >     + `mustexist`: (`False`)表名是否一定需要存在于元数据中（不存在时引发异常）
    > 
    > ##### 常用`SchemaItem`子类：
    > + `PrimaryKeyConstraint`
    > + `ForeignKeyConstraint`
    > ##### 注意，在使用不同版本的SQLAlchemy时，以上参数中：
    > + 老版本中可能部分参数还没有
    > + 新版本中可能废弃了部分参数
    > + `keep_existing`与`extend_existing`互相排斥，不能同时传递为`True`
    > + `keep_existing`与`extend_existing`适用于新建表对象；如果要创建新的表，表明已经存在于`meta.tables`中时，需要指明任意一个参数，不然会报错。
    > + `useexisting`已被废弃, 新版本使用`extend_existing`
4. ## Column的构造方法
    > `Column([name, ]type_[, **kwargs])`
    > ##### 参数说明：
    > - `name` 字段名
    > - `type_` 字段数据类型，这里的**数据类型**包括：
    >     + SQLAlchemy中常用数据类型:
    >         * 整数: `SmallInteger`、`Integer`、`BigInteger`等
    >         * 浮点数: `Float`、`Numeric`等
    >         * 文本字符串: `String`、`Text`、`Unicode`、`UnicodeText`、`CHAR`、`VARCHAR`等
    >         * 二进制字符串: `LargeBinary`、`BINARY`、`VARBINARY`等
    >         * 日期时间: `Date`、`DateTime`、`TIMESTAMP`等
    >     + `Constraint`: 约束
    >     + `ForeignKey`: 外键
    >     + `ColumnDefault`: 列默认值
    > - `kwargs`主要内容：
    >     + `autoincrement`: (`False`)是否是主键
    >     + `default`: (`None`)默认值
    >     + `index`: (`None`)索引
    >     + `nullable`: (`True`)是否可以为空(`NULL`)
    >     + `primary_key`: (`False`)是否是主键
    >     + `server_default`: (`None`)服务端(数据库中的函数)默认值
    >     + `unique`: (`False`)是否唯一
    >     + `comment`: (`None`)列注释
5. ## 通过构造方法构建Table(表)对象-示例
    * 新定义，不关联到现有数据库
        ```python
        # 定义表1
        tb_ho = Table('hello', meta_new)
        # 重新定义表（不加表存在处理参数会报错）
        tb_ho = Table('hello', meta_new, Column('name', Integer))
        # 重新定义表（扩展方式）
        tb_ho = Table('hello', meta_new, Column('name', Integer), extend_existing=True)
        print([c.name for c in tb_ho.columns])
        # 重新定义表（忽略新字段方式）
        tb_ho = Table('hello', meta_new, Column('name', String(100)), keep_existing=True)
        print(tb_ho.columns['name'])
        ```
    * 数据库中加载，反射出所有元信息
        ```python
        # 加载数据库中所有表元信息到meta中
        meta.reflect()
        # 实例化表tb_user（因为表tb_user已经存在于meta元数据中，所以默认会报错）
        tb_user = Table('tb_user', meta)
        # 实例化tb_user（扩展方式）
        tb_user = Table('tb_user', meta, extend_existing=True)
        print([c.name for c in tb_user.columns])
        # 实例化tb_user（忽略新字段方式）
        tb_user = Table('tb_user', meta, keep_existing=True)
        print(tb_ho.columns['name'])
        ```
    * 数据库中加载，不反射
        ```python
        # 定义表(虽然数据库中有数据，但是meta中还未读取，所以不会报错)
        tb_user = Table('tb_user', meta)
        ```
6. ## meta后期绑定engine，并将创建的表保存到数据库
    ```python
    tb_wd = Table(
        'world', meta_new,
        Column('id', Integer, primary_key=True),
        Column('name', String(100), unique=True),
        Column('year', Integer, default=2018),
        comment='世界'
    )
    tb_world = Table(
        'wd', meta_new,
        Column('id', Integer, primary_key=True),
        Column('name', String(100), unique=True),
        Column('year', Integer, server_default=text('2018')),
        comment='世界2'
    )
    meta_new.create_all(bind=engine, tables=[tb_wd, tb_world])

    # 添加外键
    tb_for = Table(
        'for', meta_new,
        Column('id', Integer),
        Column('world_id', ForeignKey("wd.id")),
        comment='外键'
    )
    meta_new.create_all(bind=engine, tables=[tb_for])
   ```
7. ## 数据查询（链式调用）
    ```python
    # 加载数据库中所有表元信息到meta中
    meta.reflect()
    # 得到表(映射方式)
    tb_user = meta.tables['tb_user']

    # 构造查询（所有列）
    # statement 简称 stmt，表示一段SQL语句
    stmt = tb_user.select()
    # 构造查询（指定列）
    sel_cols = [
        getattr(tb_user.columns, col_name)
        for col_name in ['username', 'password']
    ]
    stmt = stmt.with_only_columns(sel_cols)
    # 和上面等效的写法
    stmt = stmt.with_only_columns([tb_user.c.username, tb_user.c.password])
 
    # 直接执行（表的meta绑定了引擎或连接时）
    rp = stmt.execute()
    # 使用引擎执行（表的meta没有绑定引擎或连接时）
    rp = engine.execute(stmt)
 
    # 获取列
    print(rp.keys())
 
    # 获取数据
    print(rp.fetchall())
    # 迭代，打印数据行内容
    for row in rp:
        # row是sqlalchemy.engine.result.RowProxy对象
        print(row, type(row), dict(row))
 
    # 构造插入
    user_obj = dict(username='张三', password='666')
    stmt_add = tb_user.insert().values(**user_obj)
    # 和上面等效
    stmt_add = tb_user.insert().values(username='张三', password='666')

    # 执行Insert语句
    rp = stmt_add.execute()
    print(rp.rowcount)
    ```
8. ## 查看语句
    ```python
    from sqlalchemy.sql.expression import text


    def structure_sql(dialect_obj, sql_str_or_stmt, sql_params={}, return_obj=False):
        '''
        构造SQL语句
        参数:
            dialect_obj: 数据库专用术语对象
            sql_str_or_stmt: 原始（Raw）SQL字符串或Statement（Select、Insert、Update、Delete）对象
            sql_params: 参数
            return_obj: 是否返回编译对象（默认否，返回字符串）
        refer: https://stackoverflow.com/questions/5631078/sqlalchemy-print-the-actual-query#answer-45551136
        '''
        stmt = sql_str_or_stmt
        # 如果是原始字符串，则包装成 Statement 对象
        if isinstance(stmt, str):
            stmt = text(stmt)
        stmt = stmt.bindparams(**sql_params)

        full_sql = stmt.compile(
            dialect=dialect_obj,
            compile_kwargs={"literal_binds": True}
        )
        return full_sql if return_obj else full_sql.string

    # 方言、行话（此处意译为 `数据库专用术语对象`）
    # 从数据库引擎中获取
    dialect_obj = engine.dialect
    '''
    # 从SQLAlchemy中手动构造
    # 从不同数据库中导入 dialect
    from sqlalchemy.dialects.mysql import dialect
    from sqlalchemy.dialects.sqlite import dialect
    # 实例化 dialect
    dialect_obj = dialect()
    '''
    # 查询的SQL语句
    sql = '''
    SELECT *
    FROM tb_user
    WHERE id > :bp_id
    '''
    # SQL语句参数
    sql_params = {
        'bp_id': 3
    }
    # 构造SQL语句
    full_sql = structure_sql(dialect_obj, sql, sql_params)
    print(full_sql)
    ```
9.  ## 销毁引擎
    ```python
    engine.dispose()
    ```