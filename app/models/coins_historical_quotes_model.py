from app.configurations.database import db
from sqlalchemy import Column, Integer, String, Date, Float


class CoinsHistorical(db.Model):
    __tablename__ = "coins_historical"

    id = Column(Integer, primary_key=True)

    coin = Column(String(150), nullable=False)
    date = Column(Date, nullable=False)
    price = Column(Float, nullable=False)

    def serialized(self):
        return {"id": self.id, "coin": self.coin, "date": self.date, "price": self.price }
    