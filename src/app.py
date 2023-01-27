import os

from flask import Flask
from sqlalchemy_utils import create_database, database_exists
from app_controller import controller
from db import db

url = "postgresql://" + os.environ["POSTGRES_USER"] + ":" + os.environ[
    "POSTGRES_PASSWORD"] + "@" + os.environ["POSTGRES_DB"] + "/stock"

# url = "postgresql://" + "dbc" ":" + "dbc" + "@" + "localhost:5434" + "/stock"
if not database_exists(url):
    create_database(url)

app = Flask(__name__)
app.app_context().push()
app.config["SQLALCHEMY_DATABASE_URI"] = url

if __name__ == "__main__":
    db.init_app(app)
    with app.app_context():
        db.create_all()
        db.session.commit()
    app.register_blueprint(controller)
    from waitress import serve

    serve(app, host="0.0.0.0", port=7777)