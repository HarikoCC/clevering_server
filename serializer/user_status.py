from datetime import datetime

from pydantic import BaseModel

from db import StatusRecord


class UserStatus(BaseModel):
    user_id: int
    heart_rate: int
    hrv: int
    blood_oxygen: int
    concentration: int


class FindRecord(BaseModel):
    mode: int
    user_id: int
    start_time: datetime
    end_time: datetime


def user_status_dict(data: UserStatus):
    data_dict = {
        "user_id": data.user_id,
        "heart_rate": data.heart_rate,
        "hrv": data.hrv,
        "blood_oxygen": data.blood_oxygen,
        "concentration": data.concentration,
        "timestamp": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    }
    return data_dict

def record_time_dict(data: FindRecord):
    data_dict = {
        "user_id": data.user_id,
        "start_time": str(data.start_time),
        "end_time": str(data.end_time),
    }
    return data_dict


def record_dict_list(data_list: list[StatusRecord]):
    dict_list = [
        {
            "user_id": data.user_id,
            "heart_rate": data.heart_rate,
            "hrv": data.hrv,
            "blood_oxygen": data.blood_oxygen,
            "concentration": data.concentration,
            "timestamp": data.timestamp,
        }
        for data in data_list
    ]
    return dict_list
