from pydantic import BaseModel


class NormalResponse(BaseModel):
    code: int
    message: str
    data: str