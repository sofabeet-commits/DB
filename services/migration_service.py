import os
import subprocess

from sqlalchemy.orm import Session

from models import Base, WeatherData, WindData
from repositories import WeatherRepository, WindRepository
from config.database import get_session


class MigrationService:

    @staticmethod
    def run_alembic(db_url: str) -> str:
        env = os.environ.copy()
        env["DATABASE_URL"] = db_url
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            cwd=project_dir,
            env=env,
            capture_output=True,
            text=True,
        )

        output = result.stderr.strip()
        if result.returncode != 0:
            raise RuntimeError(
                f"Помилка alembic:\n{output}\n{result.stdout}"
            )
        return output

    @staticmethod
    def cross_migrate(source_url: str, target_url: str) -> dict:
        MigrationService.run_alembic(target_url)

        source_session, source_engine = get_session(source_url)
        target_session, target_engine = get_session(target_url)

        source_weather_repo = WeatherRepository(source_session)
        target_weather_repo = WeatherRepository(target_session)

        result = {"weather_count": 0, "wind_count": 0}

        try:
            weathers = source_weather_repo.get_all()
            for w in weathers:
                new_w = WeatherData(
                    id=w.id,
                    country=w.country,
                    location_name=w.location_name,
                    latitude=w.latitude,
                    longitude=w.longitude,
                    timezone=w.timezone,
                    last_updated=w.last_updated,
                    temperature_celsius=w.temperature_celsius,
                    condition_text=w.condition_text,
                    humidity=w.humidity,
                    pressure_mb=w.pressure_mb,
                    visibility_km=w.visibility_km,
                    wind_degree=w.wind_degree,
                    wind_kph=w.wind_kph,
                    wind_direction=w.wind_direction,
                    wind_mph=w.wind_mph,
                    gust_mph=w.gust_mph,
                    gust_kph=w.gust_kph,
                    sunrise=w.sunrise,
                    sunset=w.sunset,
                )
                target_session.merge(new_w)
            target_session.commit()
            result["weather_count"] = len(weathers)

            source_wind_repo = WindRepository(source_session)
            if source_wind_repo.table_exists():
                winds = source_wind_repo.get_all()
                for wd in winds:
                    new_wd = WindData(
                        id=wd.id,
                        weather_id=wd.weather_id,
                        wind_degree=wd.wind_degree,
                        wind_kph=wd.wind_kph,
                        wind_mph=wd.wind_mph,
                        wind_direction=wd.wind_direction,
                        gust_mph=wd.gust_mph,
                        gust_kph=wd.gust_kph,
                        should_go_outside=wd.should_go_outside,
                    )
                    target_session.merge(new_wd)
                target_session.commit()
                result["wind_count"] = len(winds)
        finally:
            source_session.close()
            target_session.close()

        return result
