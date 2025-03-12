import db
from db import DbSession, UserInformation


class UserSignModel(DbSession):

    def get_info_by_id(self, id: int):
        result = self.session.query(UserInformation).filte(UserInformation.user_id == id).first()
        return result

    def get_info_by_phone(self, phone: int):
        result = self.session.query(UserInformation).filte(UserInformation.user_phone == phone).first()
        return result

    def delete_by_id(self, id: int):
        result = self.session.query(UserInformation).filter(UserInformation.user_id == id).first()
        self.session.delete(result)
        self.session.commit()

    def user_sign_up(self, data: dict):
        record = UserInformation(**data)
        self.session.add(record)
        self.session.commit()