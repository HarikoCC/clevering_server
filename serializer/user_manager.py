from pydantic import BaseModel


class UserInfo(BaseModel):
    user_id: int
    user_name: str
    user_type: int
    user_phone: int
    user_password: str


class UserSignIn(BaseModel):
    sign_in_mode: int
    user_info: int
    user_password: str


class UserDelete(BaseModel):
    user_id: int
    user_password: str


def user_info_dict(data: UserInfo):
    data_dict = {
        "user_id": data.user_id,
        "user_name": data.user_name,
        "user_type": data.user_type,
        "user_phone": data.user_phone,
        "user_password": data.user_password,
    }
    return data_dict

