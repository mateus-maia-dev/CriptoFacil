from flask import Flask


def init_app(app: Flask):
    
    from app.views.user_views import user
    app.register_blueprint(user)
    from app.views.create_transactions_views import transactions
    app.register_blueprint(transactions)
    
    from app.views.portfolio_views import portfolio
    app.register_blueprint(portfolio)
    
