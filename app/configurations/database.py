from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app: Flask):
    db.init_app(app)
    app.db = db
    
    from app.models.user_model import User
    from app.models.portfolio_model import Portfolio
    from app.models.transactions_model import Transaction
    from app.models.accounting_model import Accounting
    from app.models.ptax_model import Ptax
    from app.models.coins_list_model import Coins_List

