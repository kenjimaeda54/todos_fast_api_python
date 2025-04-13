from pydantic import BaseModel


class UserRequest(BaseModel):
    email: str
    user_name: str
    first_name: str
    last_name: str
    password: str
    is_active: bool
    role: str
    