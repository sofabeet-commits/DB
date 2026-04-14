from datetime import datetime

from models import WeatherData, WindData
from repositories import WeatherRepository, WindRepository


class WeatherService:
    def __init__(
        self,
        weather_repo: WeatherRepository,
        wind_repo: WindRepository,
    ):
        self.weather_repo = weather_repo
        self.wind_repo = wind_repo

    @staticmethod
    def should_go_outside(wind_kph: float | None, gust_kph: float | None) -> bool:
        if wind_kph is not None and wind_kph > 50:
            return False
        if gust_kph is not None and gust_kph > 70:
            return False
        return True

    def populate_wind_data(self) -> int:
        if not self.wind_repo.table_exists():
            raise RuntimeError("Таблиця wind_data ще не створена!")

        existing_ids = self.wind_repo.get_existing_weather_ids()
        weathers = self.weather_repo.get_all()

        count = 0
        for w in weathers:
            if w.id not in existing_ids:
                wd = WindData(
                    weather_id=w.id,
                    wind_degree=w.wind_degree,
                    wind_kph=w.wind_kph,
                    wind_mph=w.wind_mph,
                    wind_direction=w.wind_direction,
                    gust_mph=w.gust_mph,
                    gust_kph=w.gust_kph,
                    should_go_outside=True,
                )
                self.wind_repo.add(wd)
                count += 1

        self.wind_repo.commit()
        return count

    def fill_should_go_outside(self) -> tuple[int, int]:
        if not self.wind_repo.table_exists():
            raise RuntimeError(
                "Таблиця wind_data ще не створена! "
                "Спочатку запустіть міграції."
            )

        self.populate_wind_data()

        winds = self.wind_repo.get_all()
        updated = 0
        for w in winds:
            val = self.should_go_outside(w.wind_kph, w.gust_kph)
            if w.should_go_outside != val:
                w.should_go_outside = val
                updated += 1

        self.wind_repo.commit()
        return updated, len(winds)

    def query_weather(
        self,
        country: str | None = None,
        date: datetime | None = None,
        location: str | None = None,
    ) -> list[dict]:
        results = self.weather_repo.find_by_filters(
            country=country, date=date, location=location
        )

        output = []
        for w in results:
            wind = self.wind_repo.get_by_weather_id(w.id)
            entry = {
                "country": w.country,
                "location": w.location_name,
                "last_updated": w.last_updated,
                "temperature": w.temperature_celsius,
                "condition": w.condition_text,
                "humidity": w.humidity,
                "pressure_mb": w.pressure_mb,
                "visibility_km": w.visibility_km,
                "sunrise": w.sunrise,
                "sunset": w.sunset,
                "latitude": w.latitude,
                "longitude": w.longitude,
            }
            if wind:
                entry.update({
                    "wind_kph": wind.wind_kph,
                    "wind_mph": wind.wind_mph,
                    "wind_degree": wind.wind_degree,
                    "wind_direction": wind.wind_direction,
                    "gust_kph": wind.gust_kph,
                    "gust_mph": wind.gust_mph,
                    "should_go_outside": wind.should_go_outside,
                })
            else:
                entry.update({
                    "wind_kph": w.wind_kph,
                    "wind_mph": w.wind_mph,
                    "wind_degree": w.wind_degree,
                    "wind_direction": w.wind_direction,
                    "gust_kph": w.gust_kph,
                    "gust_mph": w.gust_mph,
                    "should_go_outside": None,
                })
            output.append(entry)

        return output

    def get_statistics(self) -> dict:
        stats = {
            "weather_count": self.weather_repo.count(),
        }

        if self.wind_repo.table_exists():
            stats["wind_count"] = self.wind_repo.count()
            stats["safe_count"] = self.wind_repo.count_safe()
            stats["danger_count"] = self.wind_repo.count_danger()
        else:
            stats["wind_count"] = None

        return stats
