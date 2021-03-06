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

    def serialized(self):
        return {"id": self.id, "date": self.date, "sell_total": self.sell_total, "profit": self.profit, "tax": self.tax, "foreign_exch": self.foreign_exch, "transaction_id": self.transaction_id}
