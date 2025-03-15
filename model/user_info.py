from sqlalchemy import inspect

from db import DbSession, UserInformation


class UserModel(DbSession):

    def get_info_by_id(self, uid: int):
        result = self.session.query(UserInformation).filter(UserInformation.user_id == uid).first()
        return result

    def get_info_by_phone(self, phone: int):
        result = self.session.query(UserInformation).filter(UserInformation.user_phone == phone).first()
        return result

    def delete_by_id(self, uid: int):
        result = self.session.query(UserInformation).filter(UserInformation.user_id == uid).first()
        self.session.delete(result)
        self.session.commit()

    def user_sign_up(self, data: dict):
        record = UserInformation(**data)
        self.session.add(record)
        self.session.commit()

    def update_info(self, uid: int, data: dict):
        file = self.session.query(UserInformation).filter(UserInformation.user_id == uid).first()
        for key, value in data.items():
            setattr(file, key, value)
        self.session.commit()