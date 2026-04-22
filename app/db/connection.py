from app.config import settings
from app.db.mysql import MySQLPool


def get_db_pool():
    return MySQLPool


db_pool = get_db_pool()
