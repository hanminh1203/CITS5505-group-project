import random
import traceback

from faker import Faker
from sqlalchemy import delete

from run import app
from app.extensions import db
from app.models import (
    Offer,
    Request,
    Skill,
    User,
)

session = db.session

def clear_data():
    session.execute(delete(Offer))
    session.execute(delete(Request))
    session.execute(delete(Skill))
    session.execute(delete(User))

def main():
    try:
        clear_data()
        session.commit()
        print(
            f"Database cleaned."
        )
    except Exception as exc:
        session.rollback()
        print(f"Something happened while seeding data: {exc}")
        print(traceback.format_exc())


with app.app_context():
    main()
