import uuid

from fastapi import APIRouter, Depends

from model.user_manager import UserModel, UserRedisModel
from serializer.response import NormalResponse, DictResponse
from serializer.user_manager import UserInfo, user_info_dict, UserSignIn, UserDelete
from utils import verify_token

router = APIRouter(
    prefix="/user"
)


# 用户注册
@router.post("/signup")
async def signup(data: UserInfo):
    db = UserModel()
    result = db.get_info_by_id(data.user_id)
    if result is not None:
        return NormalResponse(code=0, message="用户注册失败", data="用户ID已存在")
    await db.user_sign_up(user_info_dict(data))
    return NormalResponse(code=0, message="用户注册成功", data="用户注册成功")


# 用户登录
@router.post("/signin")
async def signin(data: UserSignIn):
    db = UserModel()
    rds = UserRedisModel()
    if data.sign_in_mode == 0:
        result = db.get_info_by_id(data.user_info)
    else:
        result = db.get_info_by_phone(data.user_info)
    if result is None:
        return NormalResponse(code=0, message="用户登录失败", data="用户不存在")
    if result.user_password != data.user_password:
        return NormalResponse(code=0, message="用户登录失败", data="密码错误")

    if rds.exist_user(result.user_id):
        rds.delete_token(result.user_id)

    new_token = str(uuid.uuid4())
    rds.set_token(result.user_id, new_token)
    return NormalResponse(code=0, message="用户登录成功", data=new_token)


# 获取用户信息
@router.get("/info")
async def info(uid: int, _: bool = Depends(verify_token)):
    db = UserModel()
    result = db.get_info_by_id(uid)
    if result is None:
        return NormalResponse(code=0, message="信息获取失败", data="用户不存在")
    else:
        return DictResponse(code=0, message="信息获取成功", data=user_info_dict(result))


# 更新用户信息
@router.post("/update")
async def update(data: UserInfo, _: bool = Depends(verify_token)):
    db = UserModel()
    result = db.get_info_by_id(data.user_id)
    if result is not None:
        return NormalResponse(code=0, message="用户修改失败", data="用户不存在")
    await db.update_info(user_info_dict(data))
    return NormalResponse(code=0, message="用户修改成功")


# 删除用户
@router.post("/delete")
async def delete(data: UserDelete, _: bool = Depends(verify_token)):
    db = UserModel()
    rds = UserRedisModel()
    result = db.get_info_by_id(data.user_id)
    rds.delete_token(data.user_id)
    if result is None:
        return NormalResponse(code=0, message="用户删除失败", data="用户不存在")
    if result.user_password == data.user_password:
        db.delete_by_id(data.uid)
        return NormalResponse(code=0, message="用户删除成功")
    