from sqlalchemy import text
from sqlalchemy.orm import Session

from models import WindData


class WindRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, record: WindData):
        self.session.add(record)

    def commit(self):
        self.session.commit()

    def count(self) -> int:
        return self.session.query(WindData).count()

    def get_all(self) -> list[WindData]:
        return self.session.query(WindData).all()

    def get_by_weather_id(self, weather_id: int) -> WindData | None:
        return self.session.query(WindData).filter(
            WindData.weather_id == weather_id
        ).first()

    def get_existing_weather_ids(self) -> set[int]:
        rows = self.session.query(WindData.weather_id).all()
        return {r[0] for r in rows}

    def count_safe(self) -> int:
        return self.session.query(WindData).filter(
            WindData.should_go_outside == True
        ).count()

    def count_danger(self) -> int:
        return self.session.query(WindData).filter(
            WindData.should_go_outside == False
        ).count()

    def table_exists(self) -> bool:
        try:
            self.session.execute(text("SELECT 1 FROM wind_data LIMIT 1"))
            return True
        except Exception:
            self.session.rollback()
            return False
