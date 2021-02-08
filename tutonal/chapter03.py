from fastapi import APIRouter, Path, Query
from typing import Optional, List
from enum import Enum

app03 = APIRouter()
"""Path Parameters and Number Validations 路径参数和数字验证"""


@app03.get("/path/parameters")
async def path_params01():
    return {"message": "This is a message"}


@app03.get("/path/{parameters}")
async def path_params0101(parameters: str):
    return {"message": parameters}


class CityName(str, Enum):
    Beijing = "Beijing China"
    Shanghai = "Shanghai China"


@app03.get("/enum/{city}")  # 枚举类型参数
async def latest(city: CityName):
    if city == CityName.Shanghai:
        return {"city_name": city, "confirmed": 1492, "death": 7}
    elif city == CityName.Beijing:
        return {"city_name": city, "confirmed": 971, "death": 9}
    else:
        return {"city_name": city, "latest": "unknown"}


@app03.get("/files/{file_path:path}")  # 通过path parameters传递文件路径
async def filepath(file_path: str):
    return f"The file path is {file_path}"


@app03.get("/select/{num}")
async def path_params_validate(num: int = Path(...,
                                               title="你的数字",
                                               description="不可描述",
                                               ge=1,
                                               le=10)):
    return num


"""Query Parameters and String Validatings 查询参数和字符串验证"""


@app03.get("/query")
async def page_limit(page: int = 1,
                     limit: Optional[int] = None):  # 给了默认值就是默认参数，没给就是必填参数
    if limit:
        return {"page": page, "limit": limit}
    return {"page": page}


@app03.get("/query/bool/conversion")
async def type_conversion(
        param: bool = False):  # bool类型转换：yes on 1 True true会转换成true
    return param


@app03.get("/query/validations")
async def query_params_validate(
        value: str = Query(..., min_length=8, max_length=16, regex="^a"),
        values: List[str] = Query(default=["v1", "v2"]),
        alias="alias_name"):
    return value, values
