from passlib.context import CryptContext
from schema.schema import UserLoginSchema
from fastapi_sqlalchemy import db
from models.models import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher():
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)




def check_user(data: UserLoginSchema):
    db_users = db.session.query(User.email, User.password).filter_by(email=data.email).all()

    for pwd in db_users:
        verify = Hasher.verify_password(data.password, pwd[1])
        if verify:
            return True
        return False