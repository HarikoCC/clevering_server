from db import DbSession, UserStatus, StatusRecord


class UserStatusModel(DbSession):

    def get_status(self, id: int):
        result = self.session.query(UserStatus).filte(UserStatus.user_id == id).first()
        return result

    def add_status(self, data: dict):
        record = UserStatus(**data)
        self.session.add(record)
        self.session.commit()

    def alter_status(self, data: dict):
        self.session.query(UserStatus).filter(UserStatus.user_id == data["user_id"]).update()
        self.session.commit()

    # 日志
    def add_record(self, data: dict):
        record = StatusRecord(**data)
        self.session.add(record)
        self.session.commit()

    def get_record(self, id: int):
        result = self.session.query(StatusRecord).filter(StatusRecord.user_id == id).first()
        return result

    def get_record_by_time(self, data: dict):
        result = self.session.query(UserStatus).filter(
            StatusRecord.user_id == data["user_id"],
            StatusRecord.timestamp >= data["start_time"],
            StatusRecord.timestamp <= data["end_time"]
        )
        return result

    def delete_record(self, id: int):
        self.session.query(StatusRecord).filter(StatusRecord.user_id == id).delete()
        self.session.commit()

    def delete_record_by_time(self, data: dict):
        self.session.query(UserStatus).filter(
            StatusRecord.user_id == data["user_id"],
            StatusRecord.timestamp >= data["start_time"],
            StatusRecord.timestamp <= data["end_time"]
        ).delete()
        self.session.commit()
