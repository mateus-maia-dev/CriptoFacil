from app.configurations.database import db
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, ForeignKey


class Portfolio(db.Model):
    __tablename__ = "portfolio"

    id = Column(Integer, primary_key=True)

    coin = Column(String, nullable=False)
    avg_cost_brl = Column(String, nullable=False)
    avg_cost_usd = Column(String, nullable=False)
    net_quantity = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey('user.id'))

    transaction = relationship("Transaction", backref=backref("portfolio"))
