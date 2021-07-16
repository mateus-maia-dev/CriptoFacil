from flask import Flask
import json

from flask.app import Flask
from werkzeug.wrappers import response
from app.views.accounting_view import accounting
from app import views


def test_accounting_route():
    app = Flask(__name__)
    views.init_app(app)
    client = app.test_client()
    url = '/accounting'

    resp = client.get(url)
    assert resp.get_data() == b'Hello World!'
    assert resp.status_code == 200
