from fastapi import APIRouter, Depends

from model.user_group import GroupModel
from serializer.response import NormalResponse
from serializer.user_group import (group_info_list_dist, user_group_list_dist, GroupInfo, group_info_dist, \
                                   UserGroupSer, user_group_dist)
from utils import verify_token

router = APIRouter(
    prefix="/group"
)


@router.get("/list")
async def list(_: bool = Depends(verify_token)):
    db = GroupModel()
    result = db.get_group_list()
    if result is None:
        return NormalResponse(code=0, message="查询失败", data="无用户组信息")
    return NormalResponse(code=0, message="查询成功", data=group_info_list_dist(result))


@router.get("/get_group")
async def get_group(uid: int, _: bool = Depends(verify_token)):
    db = GroupModel()
    result = db.get_group_by_uid(uid)
    if result is None:
        return NormalResponse(code=0, message="查询失败", data="无用户组信息")
    return NormalResponse(code=0, message="查询成功", data=user_group_list_dist(result))


@router.get("/get_user")
async def get_user(gid: int, _: bool = Depends(verify_token)):
    db = GroupModel()
    result = db.get_user_by_gid(gid)
    if result is None:
        return NormalResponse(code=0, message="查询失败", data="无用户信息")
    return NormalResponse(code=0, message="查询成功", data=user_group_list_dist(result))


@router.post("/alter_name")
async def alter_name(gid: int, name: str, _: bool = Depends(verify_token)):
    db = GroupModel()
    db.alter_group_name(gid, name)
    return NormalResponse(code=0, message="用户组名更改成功")


@router.post("/alter_note")
async def alter_note(gid: int, note: str, _: bool = Depends(verify_token)):
    db = GroupModel()
    db.alter_group_note(gid, note)
    return NormalResponse(code=0, message="用户组备注更改成功")


@router.post("/create")
async def create(data: GroupInfo, _: bool = Depends(verify_token)):
    db = GroupModel()
    db.create_group(group_info_dist(data))
    return NormalResponse(code=0, message="用户组创建成功")


@router.post("/delete")
async def delete(gid: int, _: bool = Depends(verify_token)):
    db = GroupModel()
    db.delete_group(gid)
    return NormalResponse(code=0, message="用户组删除成功")


@router.post("/add_user")
async def add_user(data: UserGroupSer, _: bool = Depends(verify_token)):
    db = GroupModel()
    db.add_user_group(user_group_dist(data))
    return NormalResponse(code=0, message="用户已增加")


@router.post("/delete_user")
async def delete_user(uid: int, gid: int, _: bool = Depends(verify_token)):
    db = GroupModel()
    db.delete_user_group(uid, gid)
    return NormalResponse(code=0, message="用户已删除")
