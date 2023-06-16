import uvicorn
import platform
from fastapi import FastAPI
from typing import Union, Dict
from pydantic import BaseModel
from fastapi.requests import Request
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

# 关闭文档显示
app = FastAPI(docs_url=None, redoc_url=None)


# 实例化一个limiter对象，根据客户端地址进行限速
limiter = Limiter(key_func=get_remote_address)
# 指定FastApi的限速器为limiter
app.state.limiter = limiter
# 指定FastApi的异常拦截器
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


class Response(BaseModel):
    code: int
    result: Union[str, None, Dict]
    msg: str


@app.get("/")
@limiter.limit("10/minute")
async def root(request: Request):
    res = Response(code=0, result="这只是一个个人首页", msg="success")
    return res


# 根据不同环境获取配置信息 能够兼容服务器
if platform.system().lower() == "windows":
    host = "127.0.0.1"
else:
    host = "0.0.0.0"

if __name__ == '__main__':
    uvicorn.run("main:app", host=host, port=5000)