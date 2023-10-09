from core.alembic.connection import fetch_db_cred

def add_config(application):
    application.config["SQLALCHEMY_DATABASE_URI"] = fetch_db_cred()
    application.config['SECRET_KEY'] = "secret_splitwise"