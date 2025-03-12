from fastapi import APIRouter, Depends

from model.user_sign import UserSignModel
from serializer.normal_response import NormalResponse
from serializer.user_sign import UserInfo, sign_up_dict, UserSignIn, UserDelete

router = APIRouter(
    prefix="/sign"
)


@router.post("/signup")
async def signup(data: dict = Depends(sign_up_dict)):
    db = UserSignModel()
    result = db.get_info_by_id(UserInfo.user_id)
    if result is not None:
        return NormalResponse(code=1, message="用户注册失败", data="用户ID已存在")
    await db.user_sign_up(data)
    return NormalResponse(code=0, message="用户注册成功", data="用户注册成功")


@router.post("/signin")
async def signin(data: UserSignIn):
    db = UserSignModel()
    if data.sign_in_mode == 0:
        result = db.get_info_by_id(data.user_info)
    else:
        result = db.get_info_by_phone(data.user_info)
    if result is None:
        return NormalResponse(code=1, message="用户登录失败", data="用户不存在")
    if result.user_password != data.user_password:
        return NormalResponse(code=1, message="用户登录失败", data="密码错误")
    return NormalResponse(code=0, message="用户登录成功")


@router.post("/delete")
async def delete(data: UserDelete):
    db = UserSignModel()
    result = db.get_info_by_id(data.user_id)
    if result is None:
        return NormalResponse(code=1, message="用户删除失败", data="用户不存在")
    if result.user_password == data.user_password:
        db.delete_by_id(data.id)
        return NormalResponse(code=0, message="用户删除成功")