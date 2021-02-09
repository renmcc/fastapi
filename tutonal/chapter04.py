from fastapi import APIRouter, status, Form, File, UploadFile
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Union

app04 = APIRouter()
"""Response Model 响应模型"""


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    mobile: str = '10086'
    full_name: Optional[str] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    mobile: str = '10086'
    full_name: Optional[str] = None


users = {
    "user01": {
        "username": "user01",
        "password": "123123",
        "email": "user01@example.com"
    },
    "user02": {
        "username": "user02",
        "password": "123123",
        "email": "user02@example.com",
        "mobile": "110"
    }
}


@app04.post("/response_model",
            response_model=UserOut,
            response_model_exclude_unset=True)
async def response_model(user: UserIn):
    """
    response_model_exclude_unset=True 表示默认值不包含在响应体内，只包含实际传递的值
    """
    return users["user01"]


@app04.post(
    "/response_model/attributes",
    # response_model=Union[UserIn, UserOut],
    response_model=List[UserOut],
    response_model_exclude=["password"])
async def response_model_attributes(user: UserIn):
    """
    Union[UserIn，UserOut] 用户取两个模型的并集 
    response_model=List[UserOut] 响应体是一个列表
    response_model_exclude 用于必须排除某些字段
    response_model_include 必须返回某些字段
    """
    return [user, user]


"""Response Status Code 响应状态码"""


@app04.post("/status_code", status_code=status.HTTP_200_OK)
async def status_code():
    return {"status_code": status.HTTP_200_OK}


"""Form Data 表单数据处理"""


@app04.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    # return {"username": username}
    return username, password


"""Request Files 单文件、多文件上传及参数详解"""


@app04.post("/file")
async def uploadFile(file: bytes = File(...)):
    """
    使用File类 文件内容会以bytes的形式读入内存 适合上传小文件
    """
    return {"file_size": len(file)}


@app04.post("/files")
async def uploadFiles(files: List[bytes] = File(...)):
    """
    上传多个文件，用list接收
    """
    return {"files": len(files)}


@app04.post("/upload_files")
async def upload_files(files: List[UploadFile] = File(...)):
    """
    如果要上传单个文件把List去掉
    使用UpLoadFile类的优势：
    1.文件存储在内存中，使用的内存达到阈值后，将被保存到磁盘中
    2.适合于图片、视频大文件
    3.可以获取上传文件的元数据，如文件名、创建时间等
    4.有文件对象的异步接口
    5.上传的文件是python文件对象，可以使用write()、read()、seek()、close()操作
    """
    for file in files:
        contents = await file.read()
        print(contents)
    return {
        "filename": files[0].filename,
        "content_type": files[0].content_type
    }


"""[见run.py] FastAPI项目的静态文件配置"""
"""Path Operation Configuration 路径操作配置"""


@app04.post(
    "/path_operation_configuration",
    response_model=UserIn,
    tags=["Path", "Operation", "Configuration"],
    summary="This is summary",
    description="This is description",
    response_description="This is response description",
    # deprecated=True,
    status_code=status.HTTP_200_OK)
async def path_operation_configuration(user: UserIn):
    """
    Path Operation Configuration 路径操作配置
    user:用户信息
    return:返回结果
    """
    return user.dict()
