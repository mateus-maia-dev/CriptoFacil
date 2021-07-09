from app.configurations.database import db
from sqlalchemy import Column, Integer, String


class Coins_List(db.Model):
    __tablename__ = "coins_list"

    id = Column(Integer, primary_key=True)

    coin = Column(String, nullable=False)
    symbol = Column(String, nullable=False)
    name = Column(String, nullable=False)
    image = Column(String, nullable=False)
