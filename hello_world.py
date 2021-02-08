from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI()  # 这里不一定是app，名字随意


class CityInfo(BaseModel):
    province: str
    country: str
    is_affected: Optional[bool] = None  # 与bool的区别是可以不传，默认是null


# @app.get('/')
# def hello_world():
#     return {'hello': 'world'}


# @app.get('/city/{city}')
# def result(city: str, query_string: Optional[str] = None):
#     return {'city': city, 'query_string': query_string}


# @app.put('/city/{city}')
# def put_result(city: str, city_info: CityInfo):
#     return {
#         "city": city,
#         "contry": city_info.country,
#         "is_affected": city_info.is_affected
#     }

@app.get('/')
async def hello_world():
    return {'hello': 'world'}


@app.get('/city/{city}')
async def result(city: str, query_string: Optional[str] = None):
    return {'city': city, 'query_string': query_string}


@app.put('/city/{city}')
async def put_result(city: str, city_info: CityInfo):
    return {
        "city": city,
        "contry": city_info.country,
        "is_affected": city_info.is_affected
    }


if __name__ == '__main__':
    uvicorn.run(app='helloworld:app',
                host="127.0.0.1",
                port=8000,
                reload=True,
                debug=True)
