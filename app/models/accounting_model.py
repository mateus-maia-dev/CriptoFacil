from app.configurations.database import db
from sqlalchemy import Column, Integer, Float, ForeignKey, Date

class Accounting(db.Model):
    __tablename__ = "accounting"

    id = Column(Integer, primary_key=True)

    date = Column(Date, nullable=False)
    sell_total = Column(Float, nullable=False)
    profit = Column(Float, nullable=False)
    foreign_exch_total = Column(Float, nullable=False)

    transaction_id = Column(Integer, ForeignKey('transaction.id'))
