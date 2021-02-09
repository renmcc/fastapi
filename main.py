from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from tutonal import app03, app04, app05, app06, app07

app = FastAPI()

# 添加静态文件路由
# mount表示将某个目录下一个完全独立的应用挂载过来，这个不会在API交互文档中显示
app.mount(path='/coronavirus/static',
          app=StaticFiles(directory='./coronavirus/static'),
          name="static")

# 添加子路由
app.include_router(app03, prefix='/chapter03', tags=['第三章 请求参数和验证'])
app.include_router(app04, prefix='/chapter04', tags=['第四章 响应处理和FastAPI配置'])
app.include_router(app05, prefix='/chapter05', tags=['第五章 FastAPI的依赖注入系统'])
app.include_router(app06, prefix='/chapter06')
app.include_router(app07, prefix='/chapter07')
