import platform

from fastapi import FastAPI
from datetime import datetime
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from server import user_manager, user_status, file_manager

from utils import getMsTime

from const import FILE_PATH_WIN, FILE_PATH_MAC, FILE_PATH_LINUX


def check_system_type():
    system_type = platform.system()
    if system_type == "Windows":
        return FILE_PATH_WIN
    elif system_type == "Darwin":
        return FILE_PATH_MAC
    elif system_type == "Linux":
        return FILE_PATH_LINUX
    else:
        raise RuntimeError(f"Unsupported operating system: {system_type}")


app = FastAPI()

PATH = check_system_type()

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
        "timestamp": getMsTime(datetime.now())
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
        "timestamp": getMsTime(datetime.now())
    }, status_code=exc.status_code)
    return response
