from typing import Optional
from pydantic import BaseModel

# This defines what the user will be able to 'post' in the DB


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

