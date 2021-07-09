from app.configurations.database import db
from sqlalchemy import Column, Integer, String, ForeignKey, Date


class Accounting(db.Model):
    __tablename__ = "accounting"

    id = Column(Integer, primary_key=True)

    date = Column(Date, nullable=False)
    sell_total = Column(String, nullable=False)
    profit = Column(String, nullable=False)
    tax = Column(String, nullable=False)
    foreign_exch = Column(String, nullable=False)

    transaction_id = Column(Integer, ForeignKey('transaction.id'))
