from fastapi import APIRouter, BackgroundTasks, Depends
from typing import Optional

app08 = APIRouter()
"""
[见run.py] Middleware 中间件
注意：带yield的依赖退出部分的代码和后台任务会在中间件之后运行
"""
"""
[见run.py]CORS (Cors-Origin Resource Sharing) 跨域资源共享
"""
"""
Background Tasks 后台任务
"""


def bg_task(framework: str):
    with open("test.md", mode="a+") as f:
        f.write(f"## {framework} 框架精讲")


@app08.post("/background_tasks")
async def run_bg_task(framework: str, background_task: BackgroundTasks):
    """
    framework: 前端传入的后台任务参数
    background_task： 后台任务类
    """
    background_task.add_task(bg_task, framework)
    return {"message": "任务已在后台运行"}


def continue_write_readme(background_task: BackgroundTasks,
                          q: Optional[str] = None):
    if q:
        background_task.add_task(bg_task, "\n> 整体的介绍 FastAPI 快速上手开发")
    return q


@app08.post("/dependency/background_tasks")
async def dependency_run_bg_task(q: str = Depends(continue_write_readme)):
    if q:
        return {"message": "任务已经在后台运行"}
