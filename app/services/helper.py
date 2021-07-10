from flask import Flask, current_app

def init_app(model) -> None:
    current_app.db.session.add(model)
    current_app.db.session.commit()
