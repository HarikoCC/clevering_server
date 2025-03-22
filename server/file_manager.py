import os
from datetime import datetime

from fastapi import APIRouter, File, UploadFile, Depends
from starlette.responses import FileResponse

from model.file_manager import FileModel, FileRedisModel
from serializer.file_manager import file_dict_list, all_file_dict_list, create_file_dict
from serializer.response import ListResponse, NormalResponse
from utils import get_path, verify_token

router = APIRouter(
    prefix="/file"
)


# 根据用户id查询文件列表
@router.get("/list")
async def list(uid: int, _: bool = Depends(verify_token)):
    db = FileModel()
    rds = FileRedisModel()
    if rds.user_file_list_exist(uid):
        result = rds.get_user_file_list(uid)
    else:
        result = await db.get_file_list(uid)
    if result is None:
        return NormalResponse(code=0, message="获取失败", data="该用户无文件")

    if not rds.user_file_list_exist(uid):
        rds.set_user_file_list(uid, file_dict_list(result))
    return ListResponse(code=0, message="获取成功", data=file_dict_list(result))


# 根据文件名查询文件列表
@router.post("/listname")
async def listname(fname: str, _: bool = Depends(verify_token)):
    db = FileModel()
    rds = FileRedisModel()
    if rds.name_file_list_exist(fname):
        result = rds.get_name_file_list(fname)
    else:
        result = await db.get_file_list_by_name(fname)
    if result is None:
        return NormalResponse(code=0, message="获取失败", data="无该名称文件")

    if not rds.name_file_list_exist(fname):
        rds.set_name_file_list(fname, file_dict_list(result))
    return ListResponse(code=0, message="获取成功", data=file_dict_list(result))


# 显示所有文件列表
@router.get("/listall")
async def listall(_: bool = Depends(verify_token)):
    db = FileModel()
    result = await db.get_all_file_list()
    if result is None:
        return NormalResponse(code=0, message="获取失败", data="文件库无文件")
    return ListResponse(code=0, message="获取成功", data=all_file_dict_list(result))


# 创建新文件
@router.post("/create")
async def create(uid: int, file: UploadFile = File(...), _: bool = Depends(verify_token)):
    db = FileModel()
    rds = FileRedisModel()
    file_name = file.filename

    path = os.path.join(get_path() + str(uid),
                        datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
                        file_name)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        with open(path, "wb") as buffer:
            while chunk := await file.read(1024):
                buffer.write(chunk)
    except Exception as e:
        return NormalResponse(code=0, detail="文件上传失败", data=str(e))

    await db.create_file(create_file_dict([uid, file_name, path]))
    rds.delete_list_hash()
    return NormalResponse(code=0, message="文件上传成功")


# 删除文件
@router.post("/delete")
async def delete(fid: int, _: bool = Depends(verify_token)):
    db = FileModel()
    rds = FileRedisModel()
    if rds.info_exist(fid):
        result = rds.get_info(fid)
    else:
        result = await db.get_file_info(fid)
    path = result.file_path
    os.remove(path)
    await db.delete_file(fid)
    rds.delete_list_hash()
    rds.delete_info(fid)
    return NormalResponse(code=0, message="文件已删除")


# 更新文件
@router.post("/update")
async def update(fid: int, file: UploadFile = File(...), _: bool = Depends(verify_token)):
    db = FileModel()
    rds = FileRedisModel()
    if rds.info_exist(fid):
        result = rds.get_info(fid)
    else:
        result = await db.get_file_info(fid)
    if result is None:
        return NormalResponse(code=0, message="文件更新失败", data="文件不存在")

    path = result.file_path
    os.remove(path)
    try:
        with open(path, "wb") as buffer:
            while chunk := await file.read(1024):
                buffer.write(chunk)
    except Exception as e:
        return NormalResponse(code=0, message="文件更新失败", data=str(e))
    await db.update_file(fid, datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    rds.delete_info(fid)

    result = await db.get_file_info(fid)
    if not rds.info_exist(fid):
        rds.set_info(fid, result)
    return NormalResponse(code=0, message="文件更新成功")


# 下载文件
@router.post("/download")
async def download(fid: int, _: bool = Depends(verify_token)):
    db = FileModel()
    rds = FileRedisModel()
    if rds.info_exist(fid):
        result = rds.get_info(fid)
    else:
        result = await db.get_file_info(fid)
    if result is None:
        return NormalResponse(code=0, message="文件下载失败", data="文件不存在")
    if not rds.info_exist(fid):
        rds.set_info(fid, result)
    try:
        return FileResponse(result.file_path, filename=result.file_name)
    except Exception as e:
        return NormalResponse(code=0, message="文件下载失败", data=str(e))
