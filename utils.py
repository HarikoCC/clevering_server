from datetime import datetime

from starlette.responses import JSONResponse


def getMsTime(dt):
    return str(int(dt.timestamp() * 1000))


def makeResponse(data):
    response = JSONResponse({
        "code": 0,
        "message": "OK",
        "data": data,
        "timestamp": getMsTime(datetime.now())
    }, status_code=200)
    return response