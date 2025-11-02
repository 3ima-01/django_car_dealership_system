from pydantic import BaseModel


class CustomerRegisterDTO(BaseModel):
    email: str
    password: str
