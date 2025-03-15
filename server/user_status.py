from fastapi import APIRouter

from model.user_status import UserStatusModel
from serializer.response import NormalResponse, ListResponse
from serializer.user_status import user_status_dict, UserStatus, FindRecord, record_time_dict, record_dict_list

router = APIRouter(
    prefix="/status"
)


# 更新状态并添加日志
@router.post("/update")
async def update(data: UserStatus):
    db = UserStatusModel()
    result = db.get_status(data["user_id"])
    if result is None:
        db.add_status(user_status_dict(data))
        db.add_record(user_status_dict(data))
        response = NormalResponse(code=0, message="状态更新成功", data="已添加新状态")
    else:
        db.alter_status(user_status_dict(data))
        response = NormalResponse(code=0, message="状态更新成功", data="已更新原状态")
    return response


# 获取用户最新状态
@router.get("/status")
async def status(uid: int):
    db = UserStatusModel()
    result = db.get_status(uid)
    if result is None:
        return NormalResponse(code=0, message="查询失败", data="无该用户信息")
    return NormalResponse(code=0, message="查询成功", data=user_status_dict(result))


# 根据id获取用户日志
@router.get("/record")
async def record(data: FindRecord):
    db = UserStatusModel()
    if FindRecord.mode == 0:
        result = db.get_record(FindRecord.user_id)
    else:
        result = db.get_record_by_time(record_time_dict(data))

    if result is None:
        return NormalResponse(code=0, message="获取失败", data="无该用户信息")
    else:
        return ListResponse(code=0, message="获取成功", data=record_dict_list(result))


# 根据日期删除用户状态日志
@router.post("/delete")
async def delete(data: FindRecord):
    db = UserStatusModel()
    if FindRecord.mode == 0:
        db.delete_record(FindRecord.user_id)
    else:
        db.get_record_by_time(record_time_dict(data))
    return NormalResponse(code=0, message="删除成功")
