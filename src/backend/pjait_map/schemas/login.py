from pydantic import BaseModel

class LoginData(BaseModel):
    login: str
    password: str

class SignupData(BaseModel):
    login: LoginData
    name: str
    surname: str
