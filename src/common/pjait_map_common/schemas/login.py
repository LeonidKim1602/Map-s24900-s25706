from pydantic import BaseModel


class User(BaseModel):
    number: int
    password: str


class CreateUser(User):
    name: str
    surname: str
