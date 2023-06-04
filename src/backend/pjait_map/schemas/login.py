from pydantic import BaseModel


class User(BaseModel):
    login: str
    password: str


class CreateUser(User):
    name: str
    surname: str
