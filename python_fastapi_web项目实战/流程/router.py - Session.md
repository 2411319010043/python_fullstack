# router.py -> Session

* **router**里‘**拥有**’**Session**
* 真正**创建**的是 `get_db`，真正**执行**的是 **FastAPI**

## why 为什么router里要有Session？

​	router是接口，接收到的每个**HTTP**请求都应该有一个**独立**的Session，这样可以明确每个Session的开始和结束。

## how

```python
@router.post("/person")
def create_person(
	person: Person,
	db: Session = Depends(get_db)
):
    return save_person(db,person)
```

