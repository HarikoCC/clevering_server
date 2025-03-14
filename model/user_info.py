from sqlalchemy import inspect

from db import DbSession, UserInformation


class UserModel(DbSession):

    def get_info_by_id(self, id: int):
        result = self.session.query(UserInformation).filter(UserInformation.user_id == id).first()
        return result

    def get_info_by_phone(self, phone: int):
        result = self.session.query(UserInformation).filter(UserInformation.user_phone == phone).first()
        return result

    def delete_by_id(self, id: int):
        result = self.session.query(UserInformation).filter(UserInformation.user_id == id).first()
        self.session.delete(result)
        self.session.commit()

    def user_sign_up(self, data: dict):
        record = UserInformation(**data)
        self.session.add(record)
        self.session.commit()

    def update_info(self, data: dict):
        record = self.session.query(UserInformation).filter(UserInformation.user_id == data[id]).first()
        mapper = inspect(record)
        for column in mapper.attrs:
            if column.key in data and data[column.key] is not None:
                setattr(record, column.key, data[column.key])
        self.session.commit()