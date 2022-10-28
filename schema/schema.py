from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy import DefaultClause

# This defines what the user will be able to 'post' in the DB





class UserSchema(BaseModel):
    fullname: str = Field(default=None)
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)
    class Config:
        the_schema = {
            "user_demo": {
                "name": "Paulo",
                "email": "teste@teste.com",
                "password": "1234"
            }
        }

class UserLoginSchema(BaseModel):
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)
    class Config:
        the_schema = {
            "user_demo": {
                "email": "teste@teste.com",
                "password": "1234"
            }
        }




class Books(BaseModel):
    title: str
    rating: int
    author_id: int

    class Config:
        orm_mode = True


class Author(BaseModel):
    firstname: str
    lastname: str
    nationality: str

    class Config:
        orm_mode = True


class Client(BaseModel):
    firstname: str
    middlename: str
    lastname: str

    class Config:
        orm_mode = True


class Request(BaseModel):
    request_value: float
    request_amount: int
    endpoint: str

    class Config:
        orm_mode = True


class ClientDelete(BaseModel):
    client_id = int
    firstname: Optional[float]
    middlename: Optional[int]
    lastname: Optional[str]
    