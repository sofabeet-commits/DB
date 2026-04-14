from datetime import datetime

from sqlalchemy.orm import Session

from models import WeatherData


class WeatherRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, record: WeatherData):
        self.session.add(record)

    def add_all(self, records: list[WeatherData]):
        self.session.add_all(records)

    def commit(self):
        self.session.commit()

    def count(self) -> int:
        return self.session.query(WeatherData).count()

    def get_all(self) -> list[WeatherData]:
        return self.session.query(WeatherData).all()

    def get_by_id(self, record_id: int) -> WeatherData | None:
        return self.session.query(WeatherData).filter(
            WeatherData.id == record_id
        ).first()

    def find_by_country(self, country: str) -> list[WeatherData]:
        return self.session.query(WeatherData).filter(
            WeatherData.country.ilike(f"%{country}%")
        ).all()

    def find_by_country_and_date(
        self, country: str, date: datetime
    ) -> list[WeatherData]:
        return self.session.query(WeatherData).filter(
            WeatherData.country.ilike(f"%{country}%"),
            WeatherData.last_updated >= date,
            WeatherData.last_updated < date.replace(hour=23, minute=59, second=59),
        ).all()

    def find_by_filters(
        self,
        country: str | None = None,
        date: datetime | None = None,
        location: str | None = None,
    ) -> list[WeatherData]:
        query = self.session.query(WeatherData)

        if country:
            query = query.filter(WeatherData.country.ilike(f"%{country}%"))
        if location:
            query = query.filter(WeatherData.location_name.ilike(f"%{location}%"))
        if date:
            query = query.filter(
                WeatherData.last_updated >= date,
                WeatherData.last_updated < date.replace(
                    hour=23, minute=59, second=59
                ),
            )

        return query.order_by(WeatherData.last_updated).all()
