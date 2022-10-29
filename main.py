from email.policy import default
import hashlib
import os
import bcrypt
import uvicorn
from fastapi import FastAPI, HTTPException, Body, Depends
from fastapi_sqlalchemy import DBSessionMiddleware, db
from dotenv import load_dotenv

from utils.utils import charge_request
from models.models import Author, Book, Client, User
from schema.schema import Books as SchemaBook
from schema.schema import Author as SchemaAuthor
from schema.schema import Client as SchemaClient
from schema.schema import UserSchema, UserLoginSchema
from auth.jwt_handler import signJWT
from auth.jwt_bearer import jwtBearer


load_dotenv(".env")

app = FastAPI()

# adds and creates db connectivity, to perform commits and such
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])


@app.get("/", tags=["test"])
def root():
    return {"message": "Hello World"}


def check_user(data: UserLoginSchema):
    db_users = db.session.query(User).all()
    print(f'**********{db_users}')
    for user in db_users:
        if user.email == data.email and user.password == data.password:
            return True
    return False


# User signup [create new user]
@app.post("/user/signup", tags=["user"])
def user_signup(user: UserSchema = Body(default=None)):

    db_user = User(fullname=user.fullname, email=user.email, password=user.password)
    db.session.add(db_user)
    db.session.commit()
    # users.append(user)
    return signJWT(user.email)


# todo: raise HTTPexception on error
@app.post("/user/login", tags=["user"])
def user_login(user: UserLoginSchema = Body(default=None)):
    if check_user(user):
        return signJWT(user.email)
    else:
        return {
            "error": "Invalid login details."
        }


    
@app.post("/add-book/", dependencies=[Depends(jwtBearer())], response_model=SchemaBook)
def add_book(book: SchemaBook):
    db_book = Book(title=book.title, rating=book.rating, author_id=book.author_id)
    db.session.add(db_book)
    db.session.commit()
    
    return db_book

@app.post("/add-author/", dependencies=[Depends(jwtBearer())], response_model=SchemaAuthor)
def add_author(author: SchemaAuthor):
    db_author = Author(firstname=author.firstname, lastname=author.lastname, nationality=author.nationality)
    db.session.add(db_author)
    db.session.commit()

    return db_author

@app.get("/books/")
def get_books():
    charge_request(0.50, 1, "/books")
    books = db.session.query(Book).all()

    return books

@app.post("/add-client/", dependencies=[Depends(jwtBearer())], response_model=SchemaClient)
def add_client(client: SchemaClient):
    db_client = Client(firstname=client.firstname, middlename=client.middlename, lastname=client.lastname)
    db.session.add(db_client)
    db.session.commit()

    return db_client


@app.delete("/delete-user/{client_id}/")
def delete_user(client_id: int):
    client = db.session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    db.session.delete(client)
    db.session.commit()

    return {"Message": "client deleted"}







# This is to run the API without docker container, locally
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)