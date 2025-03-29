from fastapi import APIRouter, Depends
from model.user_status import UserStatusModel, UserStatusRedisModel
from serializer.response import NormalResponse, ListResponse
from serializer.user_status import user_status_dict, UserStatus, FindRecord, record_time_dict, record_dict_list
from utils import verify_token
import json

router = APIRouter(
    prefix="/status"
)

redis_model = UserStatusRedisModel()


# 更新状态并添加日志
@router.post("/update")
async def update(data: UserStatus, _: bool = Depends(verify_token)):
    db = UserStatusModel()
    rds = UserStatusRedisModel()

    result = rds.status_exist(data.user_id)
    db.add_record(user_status_dict(data))
    rds.set_status(data.user_id, user_status_dict(data))

    if result is None:
        return NormalResponse(code=0, message="状态更新成功", data="已添加新状态")
    return NormalResponse(code=0, message="状态更新成功", data="已更新原状态")


# 获取用户最新状态
@router.get("/status")
async def status(uid: int, _: bool = Depends(verify_token)):
    rds = UserStatusRedisModel()
    result = rds.get_status(uid)

    if result is None:
        return NormalResponse(code=0, message="查询失败", data="无该用户最新信息")
    return NormalResponse(code=0, message="查询成功", data=str(result))


# 根据id获取用户日志
@router.get("/record")
async def record(data: FindRecord, _: bool = Depends(verify_token)):
    db = UserStatusModel()
    if data.mode == 0:
        result = db.get_record(data.user_id)
    else:
        result = db.get_record_by_time(record_time_dict(data))

    if result is None:
        return NormalResponse(code=0, message="获取失败", data="无该用户信息")
    else:
        return ListResponse(code=0, message="获取成功", data=record_dict_list(result))


# 根据日期删除用户状态日志
@router.post("/delete")
async def delete(data: FindRecord, _: bool = Depends(verify_token)):
    db = UserStatusModel()
    rds = UserStatusRedisModel()
    if data.mode == 0:
        db.delete_record(data.user_id)
        rds.rds.hdel("user_status", str(data.user_id))
    else:
        records_to_delete = db.get_record_by_time(record_time_dict(data))
        for record in records_to_delete:
            db.delete_record(record.id)
    return NormalResponse(code=0, message="删除成功", data="删除成功")
