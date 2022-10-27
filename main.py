import uvicorn
import os
from fastapi import FastAPI, HTTPException
from fastapi_sqlalchemy import DBSessionMiddleware, db
from dotenv import load_dotenv


from models.models import Author, Book, Client, Requests
from schema.schema import Books as SchemaBook
from schema.schema import Author as SchemaAuthor
from schema.schema import Client as SchemaClient
from schema.schema import Request as SchemaRequest
from schema.schema import ClientDelete as SchemaClientDelete


load_dotenv(".env")

app = FastAPI()

# adds and creates db connectivity, to perform commits and such
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

@app.get("/")
async def root():
    return {"message": "Hello World"}


def charge_request(value, amount, endpoint):
    db_charge = Requests(request_value=value, request_amount=amount, endpoint=endpoint)
    db.session.add(db_charge)
    db.session.commit()

    return
    
@app.post("/add-book/", response_model=SchemaBook)
def add_book(book: SchemaBook):
    db_book = Book(title=book.title, rating=book.rating, author_id=book.author_id)
    db.session.add(db_book)
    db.session.commit()
    return db_book

@app.post("/add-author/", response_model=SchemaAuthor)
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

@app.post("/add-client/", response_model=SchemaClient)
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