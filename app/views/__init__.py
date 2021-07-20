from flask import Flask


def init_app(app: Flask):

    from app.views.user_views import user

    app.register_blueprint(user)
    from app.views.create_transactions_views import transactions

    app.register_blueprint(transactions)

    from app.views.accounting_view import accounting

    app.register_blueprint(accounting)

    from app.views.portfolio_views import portfolio

    app.register_blueprint(portfolio)

    from app.views.graphic_view import graphic

    app.register_blueprint(graphic)

    from app.views.charts_view import charts

    app.register_blueprint(charts)
