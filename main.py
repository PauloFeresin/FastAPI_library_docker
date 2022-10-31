import os
import uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from dotenv import load_dotenv
from api import api_router


load_dotenv(".env")

app = FastAPI()

# adds and creates db connectivity, to perform commits and such
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

app.include_router(api_router)



# This is to run the API without docker container, locally
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)