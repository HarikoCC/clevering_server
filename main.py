from datetime import datetime

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from server import user_manager, user_status, file_manager
from utils import get_ms_time, check_system

check_system()

app = FastAPI()

app.include_router(user_manager.router)
app.include_router(user_status.router)
app.include_router(file_manager.router)

origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)  # 自定义HttpRequest 请求异常
async def http_exception_handle(request, exc):
    response = JSONResponse({
        "code": exc.status_code,
        "message": str(exc.detail),
        "data": None,
        "timestamp": get_ms_time(datetime.now())
    }, status_code=exc.status_code)
    return response


# 自定义 HTTP 请求异常
@app.exception_handler(RequestValidationError)
async def request_validation_error(request, exc):
    try:
        message = str(exc.detail)
    except:
        message = "请求出错"
    response = JSONResponse({
        "code": 400,
        "message": message,
        "data": None,
        "timestamp": get_ms_time(datetime.now())
    }, status_code=exc.status_code)
    return response
