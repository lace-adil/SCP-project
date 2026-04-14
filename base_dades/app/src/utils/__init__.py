from sqlalchemy import create_engine

db_engine = create_engine("mysql+pymysql://admin:SCP!PROJECT@db/scp")

def updateDatabase():
    from os import system
    system("poetry run alembic upgrade head")