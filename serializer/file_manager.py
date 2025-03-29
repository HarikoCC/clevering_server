from datetime import datetime

from pydantic import BaseModel

from db import FileInformation


def create_file_dict(data: any):
    data_dict = {
        "file_name": data.file_name,
        "user_id": data.uid,
        "file_path": data.path,
        "create_time": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        "modify_time": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    }
    return data_dict


def file_dict_list(data_list: list[FileInformation]):
    dict_list = [
        {
            "file_id": data.file_id,
            "file_name": data.file_name,
            "create_time": str(data.create_time)
        }
        for data in data_list
    ]
    return dict_list


def all_file_dict_list(data_list: any):
    dict_list = [
        {
            "file_id": data.file_id,
            "file_name": data.file_name,
            "user_name": data.user_name,
            "create_time": str(data.create_time)
        }
        for data in data_list
    ]
    return dict_list
