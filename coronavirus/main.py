from typing import List

import requests
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request, Path, Query, status
from fastapi.templating import Jinja2Templates
from pydantic import HttpUrl
from sqlalchemy.orm import Session
from typing import Optional

from coronavirus import crud, schemas
from coronavirus.database import engine, Base, SessionLocal
from coronavirus.models import City, Data

application = APIRouter()

templates = Jinja2Templates(directory='./coronavirus/templates')

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@application.post("/create_city", response_model=schemas.ReadCity)
def create_city(request: Request,
                city: schemas.CreateCity,
                db: Session = Depends(get_db)):
    print(request)
    db_city = crud.get_city_by_name(db, name=city.province)
    if db_city:
        raise HTTPException(status_code=400, detail="City already registered")
    return crud.create_city(db=db, city=city)


@application.get("/get_city/{city}", response_model=schemas.ReadCity)
def get_city(city: str = Path(..., title="城市名称", max_length=10),
             db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db, name=city)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@application.get("/get_cities", response_model=List[schemas.ReadCity])
def get_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cities = crud.get_cities(db, skip=skip, limit=limit)
    return cities


@application.post("/create_data", response_model=schemas.ReadData)
def create_data_for_city(*,
                         city: str = Query(..., title="城市名称", max_length=10),
                         data: schemas.CreateData,
                         db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db, name=city)
    if not db_city:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="City not found")
    data = crud.create_city_data(db=db, data=data, city_id=db_city.id)
    return data


@application.get("/get_data")
def get_data(city: Optional[str] = Query(None, title="城市名称", max_length=10),
             skip: Optional[int] = Query(0, title="步长", le=0),
             limit: Optional[int] = Query(100, title="过滤", ge=0, le=1000),
             db: Session = Depends(get_db)):
    data = crud.get_data(db, city=city, skip=skip, limit=limit)
    return data


def bg_task(url: HttpUrl, db: Session):
    """这里注意一个坑，不要在后台任务的参数中db: Session = Depends(get_db)这样导入依赖"""

    city_data = requests.get(
        url=f"{url}?source=jhu&country_code=CN&timelines=false")

    if 200 == city_data.status_code:
        db.query(City).delete()  # 同步数据前先清空原有的数据
        db.commit()
        for location in city_data.json()["locations"]:
            city = {
                "province": location["province"],
                "country": location["country"],
                "country_code": "CN",
                "country_population": location["country_population"]
            }
            crud.create_city(db=db, city=schemas.CreateCity(**city))

    coronavirus_data = requests.get(
        url=f"{url}?source=jhu&country_code=CN&timelines=true")

    if 200 == coronavirus_data.status_code:
        db.query(Data).delete()
        db.commit()
        for city in coronavirus_data.json()["locations"]:
            db_city = crud.get_city_by_name(db=db, name=city["province"])
            for date, confirmed in city["timelines"]["confirmed"][
                    "timeline"].items():
                data = {
                    "date": date.split("T")
                    [0],  # 把'2020-12-31T00:00:00Z' 变成 ‘2020-12-31’
                    "confirmed": confirmed,
                    "deaths": city["timelines"]["deaths"]["timeline"][date],
                    "recovered": 0  # 每个城市每天有多少人痊愈，这种数据没有
                }
                # 这个city_id是city表中的主键ID，不是coronavirus_data数据里的ID
                crud.create_city_data(db=db,
                                      data=schemas.CreateData(**data),
                                      city_id=db_city.id)


@application.get("/sync_coronavirus_data/jhu")
def sync_coronavirus_data(background_tasks: BackgroundTasks,
                          db: Session = Depends(get_db)):
    """从Johns Hopkins University同步COVID-19数据"""
    background_tasks.add_task(
        bg_task, "https://coronavirus-tracker-api.herokuapp.com/v2/locations",
        db)
    return {"message": "正在后台同步数据..."}


@application.get("/")
def coronavirus(request: Request,
                city: str = None,
                skip: int = 0,
                limit: int = 100,
                db: Session = Depends(get_db)):
    data = crud.get_data(db, city=city, skip=skip, limit=limit)
    return templates.TemplateResponse(
        "home.html", {
            "request": request,
            "data": data,
            "sync_data_url": "/coronavirus/sync_coronavirus_data/jhu"
        })
