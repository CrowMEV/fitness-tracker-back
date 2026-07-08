import re
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic.functional_validators import AfterValidator


def check_password(password: str) -> str:
    assert len(password) >= 8, "Password is shorter than 8 characters"
    assert not re.search(
        r"[а-яА-Я]", password
    ), "Password must contain only English letters"
    return password


Password = Annotated[str, AfterValidator(check_password)]


class Token(BaseModel):
    token: str


class UserLogin(BaseModel):
    email: EmailStr
    password: Password


class User(BaseModel):
    name: str
    email: EmailStr
    is_trainer: bool = False


class UserResponse(User):
    id: int
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


class CreateUser(User):
    password: Password


class UpdatePassword(BaseModel):
    current_password: Password | None = None
    password: Password | None = None
