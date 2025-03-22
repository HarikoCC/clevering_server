import datetime
import json

from db import DbSession, FileInformation
from rds import RedisSession
from serializer.user_manager import UserInfo


class FileModel(DbSession):

    def get_file_list(self, uid: int):
        result = self.session.query(FileInformation).filter(FileInformation.user_id == uid)
        return result

    def get_all_file_list(self):
        result = self.session.query(FileInformation).join(UserInfo, FileInformation.user_id == UserInfo.id)
        return result

    def get_file_list_by_name(self, fname: str):
        result = self.session.query(FileInformation).join(UserInfo, FileInformation.user_id == fname)
        return result

    def get_file_info(self, fid: int):
        result = self.session.query(FileInformation).filter(FileInformation.file_id == fid).first()
        return result

    def create_file(self, data: dict):
        record = FileInformation(**data)
        self.session.add(record)
        self.session.commit()

    def delete_file(self, fid: int):
        result = self.session.query(FileInformation).filter(FileInformation.file_id == fid).first()
        self.session.delete(result)
        self.session.commit()

    def update_file(self, fid: int, time: datetime):
        (self.session.query(FileInformation).filter(FileInformation.file_id == fid)
         .update({FileInformation.modify_time: time}))
        self.session.commit()


import json


class FileRedisModel(RedisSession):

    def user_file_list_exist(self, uid: int):
        return self.rds.hexists("user_file", str(uid))

    def get_user_file_list(self, uid: int):
        data = self.rds.hget("user_file", str(uid))
        return json.loads(data) if data else []

    def set_user_file_list(self, uid: int, file_list: list):
        self.rds.hset("user_file", str(uid), json.dumps(file_list))

    def delete_user_file_list(self, uid: int):
        self.rds.hdel("user_file", str(uid))

    def name_file_list_exist(self, name: str):
        return self.rds.hexists("name_file", name)

    def get_name_file_list(self, name: str):
        data = self.rds.hget("name_file", name)
        return json.loads(data) if data else []

    def set_name_file_list(self, name: str, file_list: list):
        self.rds.hset("name_file", name, json.dumps(file_list))

    def delete_name_file_list(self, name: str):
        self.rds.hdel("name_file", name)

    def delete_list_hash(self):
        self.rds.delete("user_file", "name_file")

    def info_exist(self, fid: int):
        return self.rds.hexists("fid", str(fid))

    def get_info(self, fid: int) -> dict:
        data = self.rds.hget("fid", str(fid))
        return json.loads(data) if data else []

    def set_info(self, fid: int, info: dict):
        self.rds.hset("fid", str(fid), json.dumps(info))

    def delete_info(self, fid: int):
        self.rds.hdel("fid", str(fid))

