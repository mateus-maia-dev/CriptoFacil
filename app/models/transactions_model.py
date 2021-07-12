from app.configurations.database import db
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, ForeignKey, Date


class Transaction(db.Model):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True)

    date = Column(Date, nullable=False)
    type = Column(String, nullable=False)
    coin = Column(String, nullable=False)
    fiat = Column(String, nullable=False)
    price_per_coin = Column(String, nullable=False)
    quantity = Column(String, nullable=False)
    brazilian_exch = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey('user.id'))

    # accounting = relationship("Transaction", backref=backref("accounting"))
