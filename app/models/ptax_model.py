from app.configurations.database import db
from sqlalchemy import Column, Integer, String, Date


class Ptax(db.Model):
    __tablename__ = "ptax"

    id = Column(Integer, primary_key=True)

    data = Column(Date, nullable=False)
    sell_rate = Column(String, nullable=False)
