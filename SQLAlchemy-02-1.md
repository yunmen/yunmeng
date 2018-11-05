# Table（表）类方式 - 数据库加载
```python
from sqlalchemy import create_engine

# 导入元数据、表类
from sqlalchemy import MetaData, Table
```

1. ## 创建引擎
    ```python
    uri = 'mysql+pymysql://root:root@127.0.0.1:3306/user_system?charset=utf8'
    engine = create_engine(uri)
    ```

2. ## 构建元数据
    ```python
    # 元数据: 主要是指数据库表结构、关联等信息
    # 实例化MetaData(从引擎读取元数据)
    meta = MetaData(bind=engine)
    ```
3. ## 自动加载
    * ### 加载单张表
        ```python
        # 加载 tb_user 表数据
        tb_user = Table('tb_user', meta, autoload=True, autoload_with=engine)
        # 获取表的列列表
        cols = tb_user.columns
        print(cols)
        # 获取表的列列名列表
        col_names = [col.name for col in cols]
        print(col_names)
        ```
    * ### 加载出所有表
        ```python
        # 加载数据库中所有表元信息
        meta.reflect()
        # 获取所有的表名列表
        table_names = [name for name in meta.tables]
        print(table_names)
        # 通过表名获取具体表对象
        tb_user = meta.tables['tb_user']
        ```
    *  ### 反射器方式加载（不使用`MetaData`）
        ```python
        from sqlalchemy.engine import reflection

        # 创建反射器
        insp = reflection.Inspector.from_engine(engine)
        # 获取表名列表
        print(insp.get_table_names())
        # 获取某个表的字段列表
        print(insp.get_columns('tb_user'))
        # 获取某个表的外键列表
        print(insp.get_foreign_keys('tb_user'))
        # 获取某个表的主键信息
        print(insp.get_pk_constraint('tb_user'))
        # 获取某个表的注释信息
        print(insp.get_table_comment('tb_user'))
        # 获取视图名列表
        print(insp.get_view_names())
        ```
    * 注意：
        - 元数据(`MetaData`)方式加载，主要用于数据库(结构和数据)操作
        - 反射器(`Inspector`)方式加载，主要用于数据库信息获取
4. ## 销毁引擎
    ```python
    engine.dispose()
    ```