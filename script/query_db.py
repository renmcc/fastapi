import sys
import os
from pathlib import Path

project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, project_dir)

from coronavirus.models import City, Data
from coronavirus.database import SessionLocal
from sqlalchemy.orm import Session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def query_db():
    try:
        db = SessionLocal()
        db.query(Data).delete()
        db.commit()
        # a = db.query(City).filter(City.province == 'Beijing').first()
        # print(a.__dict__)
    finally:
        db.close()


query_db()
