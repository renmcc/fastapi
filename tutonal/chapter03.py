from fastapi import APIRouter, Path
from typing import Optional
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
