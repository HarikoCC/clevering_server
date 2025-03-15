from pydantic import BaseModel


class NormalResponse(BaseModel):
    code: int
    message: str
    data: str


class DictResponse(BaseModel):
    code: int
    message: str
    data: dict


class ListResponse(BaseModel):
    code: int
    message: int
    data: list[dict]