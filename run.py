from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from tutonal import app03, app04, app05, app06, app07
from coronavirus import application

# from fastapi.exceptions import RequestValidationError
# from fastapi.responses import PlainTextResponse
# from fastapi.exceptions import HTTPException
# # from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(title="FastAPI Tutorial and Coronavirus Tracker API Docs",
              description="FastAPI教程 新冠病毒疫情跟踪器API接口文档",
              version="1.0.0",
              docs_url="/docs",
              redoc_url="/redocs")

# # 重写HTTPException异常处理器
# @app.exception_handler(HTTPException)
# async def http_exception_handler(request, exc):
#     """
#     request 参数不能省略
#     """
#     return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

# # 重写RequestValidationError异常处理器
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     """
#     request 参数不能省略
#     """
#     return PlainTextResponse(str(exc), status_code=exc.status_code)

# 添加静态文件路由
# mount表示将某个目录下一个完全独立的应用挂载过来，这个不会在API交互文档中显示
app.mount(path='/static',
          app=StaticFiles(directory='./coronavirus/static'),
          name="static")

# 添加子路由
app.include_router(app03, prefix='/chapter03', tags=['第三章 请求参数和验证'])
app.include_router(app04, prefix='/chapter04', tags=['第四章 响应处理和FastAPI配置'])
app.include_router(app05, prefix='/chapter05', tags=['第五章 FastAPI的依赖注入系统'])
app.include_router(app06, prefix='/chapter06', tags=["第六章 安全、认证和授权"])
app.include_router(app07,
                   prefix='/chapter07',
                   tags=["第七章 FastAPI的数据库操作和多应用的目录结构设计"])
app.include_router(application, prefix='/coronavirus', tags=['新冠病毒疫情跟踪器API'])


