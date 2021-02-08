from fastapi import FastAPI
from tutonal import app03, app04, app05, app06, app07


app = FastAPI()

# 添加子路由
app.include_router(app03, prefix='/chapter03', tags=['第三章 请求参数和验证'])
app.include_router(app04, prefix='/chapter04', tags=['第四章 响应处理和FastAPI配置'])
app.include_router(app05, prefix='/chapter05', tags=['第五章 FastAPI的依赖注入系统'])
app.include_router(app06, prefix='/chapter06')
app.include_router(app07, prefix='/chapter07')

