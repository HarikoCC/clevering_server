import datetime

from db import DbSession, FileInformation
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
