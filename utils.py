import platform

from const import FILE_PATH_WIN, FILE_PATH_MAC, FILE_PATH_LINUX
from model.user_manager import UserRedisModel
from serializer.response import NormalResponse


def get_ms_time(dt):
    return str(int(dt.timestamp() * 1000))


def get_path():
    system_type = platform.system()
    if system_type == "Windows":
        return FILE_PATH_WIN
    elif system_type == "Darwin":
        return FILE_PATH_MAC
    elif system_type == "Linux":
        return FILE_PATH_LINUX


def check_system():
    system_type = platform.system()
    if system_type not in ["Windows", "Darwin", "Linux"]:
        raise RuntimeError(f"Unsupported operating system: {system_type}")


async def verify_token(uid: int, token: str):
    rds = UserRedisModel()
    if rds.exist_user(uid):
        result = rds.get_token(uid)
    else:
        return NormalResponse(code=0, message="访问被拒绝", data="请先登录")

    if result is not token:
        return NormalResponse(code=0, message="访问被拒绝", data="请先登录")
