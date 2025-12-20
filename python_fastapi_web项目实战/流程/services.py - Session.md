# services.py -> Session

* **services**里**‘使用’**(消费)**Session**
* 你每一次对**数据库**的**增删改查**，都必须发生在一个 **Session** 里。

## what

* ### Session 到底是什么？（非常关键）

  #### 用一句“人话”：

  > **Session 是 SQLAlchemy 用来管理一次数据库操作过程的“管家”**
  >
  > **Session** 是 **ORM** 和**数据库**连接之间的**中介**

  它负责：

  - 建立数据库连接
  - 记录你做了哪些修改
  - 决定什么时候提交 / 回滚
  - 把查询结果变成 Python 对象

## how

* 一个最小可写模板

  ```python
  def some_db_action(db: Session):
      # 1. 查询
      obj = db.query(Model).first()
      # 2. 修改
      obj.xxx = 'new'
      # 3. 提交
      db.commit()
      
      return obj
  ```

## why

* 为什么“每个函数”都要传 `db: Session`?

  因为 **数据库操作必须知道： “我现在属于哪一次会话？”**

