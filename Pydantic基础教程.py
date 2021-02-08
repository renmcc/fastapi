from pydantic import BaseModel, ValidationError, constr
from datetime import datetime, date
from typing import List, Optional
from pathlib import Path
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base


class User(BaseModel):
    id: int
    name: str = 'John Snow'
    signup_ts: Optional[datetime] = None
    friends: List[int] = []


external_data = {
    "id": 123,
    "signup_ts": "2020-12-22 12:22",
    "friends": [1, 2, 2, "222"]
}

user = User(**external_data)

try:
    User(id=1, signup_ts=datetime.today(), friends=[1, 2, 3, 'abc'])
except ValidationError as e:
    print(e.json())

# 各种解析方法
print(user.dict())
print(user.json())
print(User.parse_obj(obj=external_data))
print(
    User.parse_raw(
        '{"id": 123, "name": "John Snow", "signup_ts": "2020-12-22T12:22:00", "friends": [1, 2, 2, 222]}'
    ))

path = Path('pydantic_tutorial.json')
path.write_text(
    '{"id": 123, "name": "John Snow", "signup_ts": "2020-12-22T12:22:00", "friends": [1, 2, 2, 222]}'
)
# 解析文件
print(User.parse_file(path))

# 解析返回更多信息
print(user.schema())
print(user.schema_json())

# 不做校验,不建议使用
print(
    User.construct(
        '{"id": "err", "name": "John Snow", "signup_ts": "2020-12-22 12:22:00", "friends": [1, 2, 2, 222]}'
    ))

# 查看所有字段
print(User.__fields__.keys())

################################################################继承


class Sound(BaseModel):
    sound: str


class Dog(BaseModel):
    birthday: date
    weight: float = Optional[None]
    sound: List[Sound]  # 不同的狗有不同的叫声，递归模型（Recursive Models）就是指一个嵌套一个


dogs = Dog(birthday=date.today(),
           weight=6.66,
           sound=[{
               "sound": "wang wang ~"
           }, {
               "sound": "ying ying ~"
           }])

print(dogs.dict())

###############################################################ORM模型：从类实例创建符合ORM对象的模型

Base = declarative_base()


class CompanyOrm(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True, nullable=False)
    public_key = Column(String(20), index=True, nullable=False, unique=True)
    name = Column(String(63), unique=True)
    domains = Column(ARRAY(String(255)))


class CompanyMode(BaseModel):
    id: int
    public_key: constr(max_length=20)
    name: constr(max_length=63)
    domains: List[constr(max_length=255)]

    class Config:
        orm_mode = True


co_orm = CompanyOrm(id=123,
                    public_key='foobar',
                    name='Testing',
                    domains=['example.com', 'imooc.com'])

print(CompanyMode.from_orm(co_orm))
