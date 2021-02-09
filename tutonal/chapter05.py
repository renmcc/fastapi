from fastapi import APIRouter, Depends
from typing import Optional

app05 = APIRouter()
"""Dependencies 创建、导入和声明依赖"""


async def common_parameters(q: Optional[str] = None,
                            page: int = 1,
                            limit: int = 10):
    return {"q": q, "page": page, "limit": limit}


@app05.get("/dependency01")
async def dependency01(commons: dict = Depends(common_parameters)):
    return commons


@app05.get("/dependency02")
def dependency02(commons: dict = Depends(common_parameters)):
    return commons


"""Classes as Dependencies 类作为依赖项"""
fake_items_db = [{
    "item_name": "Foo"
}, {
    "item_name": "Bar"
}, {
    "item_name": "Baz"
}]


class CommonQueryParams:
    def __init__(self,
                 q: Optional[str] = None,
                 page: int = 1,
                 limit: int = 10):
        self.q = q
        self.page = page
        self.limit = limit


@app05.get("/classes_as_dependencies")
# 类作为查询参数有三种写法
# async def classes_as_dependencies(commons: CommonQueryParams = Depends(CommonQueryParams)):
# async def classes_as_dependencies(commons: CommonQueryParams = Depends()):
async def classes_as_dependencies(commons=Depends(CommonQueryParams)):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.page:commons.page + commons.limit]
    response.update({"items": items})
    return response


"""Sub-dependencies 子依赖"""


def query(q: Optional[str] = None):
    return q


def sub_query(q: str = Depends(query), last_query: Optional[str] = None):
    if not q:
        return last_query
    return q


@app05.get("/sub_dependency")
async def sub_dependency(final_query: str = Depends(sub_query,
                                                    use_cache=True)):
    """use_cache默认是True,表示当多个依赖有一个共同的子依赖时，每次request请求只会调用子依赖一次"""
    return {"sub_dependency": final_query}
