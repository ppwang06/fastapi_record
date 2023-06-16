import uvicorn
import platform
from fastapi import FastAPI
from typing import Union, Dict
from pydantic import BaseModel


class Response(BaseModel):
    code: int
    result: Union[str, None, Dict]
    msg: str


# 关闭文档显示
app = FastAPI(docs_url=None, redoc_url=None)


@app.get("/")
async def root():
    res = Response(code=0, result="这只是一个个人首页", msg="success")
    return res


# 根据不同环境获取配置信息 能够兼容服务器
if platform.system().lower() == "windows":
    host = "127.0.0.1"
else:
    host = "0.0.0.0"

if __name__ == '__main__':
    uvicorn.run("main:app", host=host, port=5000)