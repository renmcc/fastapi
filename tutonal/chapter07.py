from fastapi import APIRouter, Request, Depends
"""Bigger Applications - Multiple Files 多应用的目录结构设计"""


async def get_user_agent(request: Request):
    print(request.headers["User-Agent"])


app07 = APIRouter(prefix="/bigger_applications",
                  tags=["第七章 FastAPI的数据库操作和多应用的目录结构设计"],
                  dependencies=[Depends(get_user_agent)],
                  responses={200: {
                      "description": "Good job!"
                  }})


@app07.get("/bigger_application")
async def bigger_application():
    return {"message": "Bigger Application"}
