from flask import Flask

def init_app(app: Flask):
    
    from app.views.register_user_views import user
    app.register_blueprint(user)
    
    from app.views.create_transactions_views import transactions
    app.register_blueprint(transactions)
    