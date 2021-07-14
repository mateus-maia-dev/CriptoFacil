from app.configurations.database import db
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Float


class Transaction(db.Model):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True)

    date = Column(Date, nullable=False)
    type = Column(String, nullable=False)
    coin = Column(String, nullable=False)
    fiat = Column(String, nullable=False)
    price_per_coin = Column(Float, nullable=False)
    avg_price_brl = Column(Float, nullable=False)
    avg_price_usd = Column(Float, nullable=False)
    net_quantity = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    foreign_exch = Column(Boolean, nullable=False)

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    accounting = relationship(
        "Accounting", uselist=False, backref=backref("transaction")
    )

    def serialized(self):
        return {
            "id": self.id,
            "date": self.date,
            "type": self.type,
            "coin": self.coin,
            "fiat": self.fiat,
            "price_per_coin": self.price_per_coin,
            "avg_price_brl": self.avg_price_brl,
            "avg_price_usd": self.avg_price_usd,
            "net_quantity": self.net_quantity,
            "quantity": self.quantity,
            "foreign_exch": self.foreign_exch,
        }
