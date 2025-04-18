from pydantic import BaseModel


class UserPasswordRequest(BaseModel):
    new_password: str
    old_password: str