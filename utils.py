import platform
from datetime import datetime

from starlette.responses import JSONResponse

from const import FILE_PATH_WIN, FILE_PATH_MAC, FILE_PATH_LINUX


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
