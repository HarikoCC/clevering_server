from db import DbSession, GroupInformation, UserGroup


class GroupModel(DbSession):

    def get_group_list(self):
        result = self.session.quary(GroupInformation)
        return result

    def alter_group_name(self, gid: int, name: str):
        group = self.session.query(GroupInformation).filter(GroupInformation.group_id == gid).first()
        setattr(group, "group_name", name)
        self.session.commit()

    def alter_group_note(self, gid: int, note: str):
        group = self.session.query(GroupInformation).first()
        setattr(group, "group_note", note)
        self.session.commit()

    def create_group(self, data: dict):
        record = GroupInformation(**data)
        self.session.add(record)
        self.session.commit()

    def delete_group(self, gid: int):
        result = self.session.query(GroupInformation).filter(GroupInformation.group_id == gid).first()
        self.session.delete(result)
        self.session.commit()

    def get_group_by_uid(self, uid: int):
        result = self.session.query(GroupInformation).join(UserGroup, GroupInformation.group_id == UserGroup.group_id).filter(UserGroup.user_id == uid)
        return result

    def get_user_by_gid(self, gid: int):
        result = self.session.query(GroupInformation).join(UserGroup, GroupInformation.group_id == UserGroup.group_id).filter(UserGroup.group_id == gid)
        return result

    def add_user_group(self, data: dict):
        record = UserGroup(**data)
        self.session.add(record)
        self.session.commit()

    def delete_user_group(self, uid: int, gid: int):
        result = (self.session.query(UserGroup)
                  .filter(UserGroup.user_id == uid, UserGroup.group_id == gid).first())
        self.session.delete(result)
        self.session.commit()
