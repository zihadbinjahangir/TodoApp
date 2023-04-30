from pydantic import BaseModel

class UserSchema(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    hashed_password: str
    is_active: bool