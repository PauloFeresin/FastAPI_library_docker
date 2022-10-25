from pydantic import BaseModel

# This defines what the user will be able to 'post' in the DB


class Books(BaseModel):
    title: str
    rating: int
    author_id: int

    class Config:
        orm_mode = True


class Author(BaseModel):
    name: str
    age: int

    class Config:
        orm_mode = True