from models.models import Requests
from fastapi_sqlalchemy import db


def charge_request(value, amount, endpoint):
    db_charge = Requests(request_value=value, request_amount=amount, endpoint=endpoint)
    db.session.add(db_charge)
    db.session.commit()

    return