from fastapi import APIRouter, Path, Query
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field
from datetime import date

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


"""Request Body and Fields 请求体和字段"""


class CityInfo(BaseModel):
    name: str = Field(..., example="Beijing")  # example是注释作用，值不会被验证
    country: str
    country_code: str = None
    country_population: int = Field(default=800,
                                    title="人口数量",
                                    description="国家的人口数量",
                                    ge=800)

    class Config:
        schema_extra = {
            "example": {
                "name": "Shanghai",
                "country": "China",
                "country_code": "CN",
                "country_population": 1400000000
            }
        }


@app03.post("/request_body/city")
async def city_info(city: CityInfo):
    return city.json()


"""Request Body + Path parameters + Query parameters 多参数混合"""


@app03.put("/request_body/city/{name}")
async def mix_city_info(name: str,
                  city01: CityInfo,
                  city02: CityInfo,  # Body可以定义多个， 下面是查询参数
                  confirmed: int = Query(ge=0, description="确诊数", default=0),   
                  death: int = Query(ge=0, description="死亡数", default=0)):
    if name == "Shanghai":
        return {"Shanghai": {"confirmed": confirmed, "death": death}}
    return city01.dict(), city02.dict()


"""Request Body - Nested Models 数据格式嵌套的请求体"""


class Data(BaseModel):
    city: List[CityInfo] = None   # 这里就是定义数据格式嵌套的请求体
    date: date  # 额外的数据类型还有uuid,datetime bytes frozenset等
    confirmed: int = Field(ge=0, description="确诊数", default=0)
    deaths: int = Field(ge=0, description="死亡数", default=0)
    recovered: int = Field(ge=0, description="痊愈数", default=0)


@app03.put("/request_body/nested")
async def nested_models(data: Data):
    return data

