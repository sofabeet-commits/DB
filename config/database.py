import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URL = os.getenv("DATABASE_URL", "sqlite:///weather.db")

TARGET_DB_URL = os.getenv("TARGET_DATABASE_URL", "sqlite:///weather_target.db")

CSV_PATH = os.getenv("CSV_PATH", os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "GlobalWeatherRepository.csv"
))


def get_engine(db_url=None):
    url = db_url or DB_URL
    return create_engine(url, echo=False)


def get_session(db_url=None):
    engine = get_engine(db_url)
    Session = sessionmaker(bind=engine)
    return Session(), engine
