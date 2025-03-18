from pydantic import BaseModel


class GroupInfo(BaseModel):
    group_id: int
    group_name: str
    group_note: str


class UserGroupSer(BaseModel):
    user_id: int
    group_id: int
    user_identity: str


class UserGroupSerDel(BaseModel):
    user_id: int
    group_id: int
    user_identity: str


def group_info_dist(data: GroupInfo):
    data_dict = {
        "group_id": data.group_id,
        "group_name": data.group_name,
        "group_note": data.group_note
    }
    return data_dict


def user_group_dist(data: UserGroupSer):
    data_dict = {
        "user_id": data.user_id,
        "group_id": data.group_id,
        "user_identity": data.user_identity,
    }
    return data_dict


def group_info_list_dist(data_list: any):
    dict_list = [
        {
            "group_id": data.group_id,
            "group_name": data.group_name,
            "group_note": data.group_note
        }
        for data in data_list
    ]
    return dict_list


def user_group_list_dist(data_list: any):
    dict_list = [
        {
            "group_id": data.group_id,
            "group_name": data.group_name,
            "group_note": data.group_note,
            "user_id": data.user_id,
            "user_name": data.group_name,
            "user_identity": data.user_identity
        }
        for data in data_list
    ]
    return dict_list
