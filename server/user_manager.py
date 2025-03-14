from fastapi import APIRouter

from model.user_info import UserModel
from serializer.response import NormalResponse, DictResponse
from serializer.user_manager import UserInfo, user_info_dict, UserSignIn, UserDelete

router = APIRouter(
    prefix="/user"
)


@router.post("/signup")
async def signup(data: UserInfo):
    db = UserModel()
    result = db.get_info_by_id(data.user_id)
    if result is not None:
        return NormalResponse(code=0, message="用户注册失败", data="用户ID已存在")
    await db.user_sign_up(user_info_dict(data))
    return NormalResponse(code=0, message="用户注册成功", data="用户注册成功")


@router.post("/signin")
async def signin(data: UserSignIn):
    db = UserModel()
    if data.sign_in_mode == 0:
        result = db.get_info_by_id(data.user_info)
    else:
        result = db.get_info_by_phone(data.user_info)
    if result is None:
        return NormalResponse(code=0, message="用户登录失败", data="用户不存在")
    if result.user_password != data.user_password:
        return NormalResponse(code=0, message="用户登录失败", data="密码错误")
    return NormalResponse(code=0, message="用户登录成功")


@router.get("/info")
async def info(id: int):
    db = UserModel()
    result = db.get_info_by_id(id)
    if result is None:
        return NormalResponse(code=0, message="信息获取失败", data="用户不存在")
    else:
        return DictResponse(code=0, message="信息获取成功", data=user_info_dict(result))


@router.post("/update")
async def update(data: UserInfo):
    db = UserModel()
    result = db.get_info_by_id(data.user_id)
    if result is not None:
        return NormalResponse(code=0, message="用户修改失败", data="用户不存在")
    await db.update_info(user_info_dict(data))
    return NormalResponse(code=0, message="用户修改成功")


@router.post("/delete")
async def delete(data: UserDelete):
    db = UserModel()
    result = db.get_info_by_id(data.user_id)
    if result is None:
        return NormalResponse(code=0, message="用户删除失败", data="用户不存在")
    if result.user_password == data.user_password:
        db.delete_by_id(data.id)
        return NormalResponse(code=0, message="用户删除成功")
