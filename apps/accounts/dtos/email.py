from pydantic import BaseModel


class EmailVerifyDTO(BaseModel):
    email: str
    token: str
