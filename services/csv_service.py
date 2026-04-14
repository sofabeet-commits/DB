import csv
import os
from datetime import datetime

from models import WeatherData
from repositories import WeatherRepository


class CsvService:
    def __init__(self, weather_repo: WeatherRepository):
        self.weather_repo = weather_repo

    def load_csv(self, csv_path: str) -> int:
        if not os.path.exists(csv_path):
            raise FileNotFoundError(
                f"Файл не знайдено: {csv_path}\n"
                "Завантажте з: https://www.kaggle.com/datasets/"
                "nelgiriyewithana/global-weather-repository"
            )

        count = 0
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                record = self._row_to_model(row)
                self.weather_repo.add(record)
                count += 1

        self.weather_repo.commit()
        return count

    def _row_to_model(self, row: dict) -> WeatherData:
        return WeatherData(
            country=row.get("country", "Unknown"),
            location_name=row.get("location_name"),
            latitude=self._parse_float(row.get("latitude")),
            longitude=self._parse_float(row.get("longitude")),
            timezone=row.get("timezone"),
            last_updated=self._parse_datetime(row.get("last_updated")),
            temperature_celsius=self._parse_float(row.get("temperature_celsius")),
            condition_text=row.get("condition_text"),
            humidity=self._parse_int(row.get("humidity")),
            pressure_mb=self._parse_float(row.get("pressure_mb")),
            visibility_km=self._parse_float(row.get("visibility_km")),
            wind_kph=self._parse_float(row.get("wind_kph")),
            wind_mph=self._parse_float(row.get("wind_mph")),
            wind_degree=self._parse_int(row.get("wind_degree")),
            wind_direction=row.get("wind_direction", "").strip() or None,
            gust_mph=self._parse_float(row.get("gust_mph")),
            gust_kph=self._parse_float(row.get("gust_kph")),
            sunrise=self._parse_time(row.get("sunrise")),
            sunset=self._parse_time(row.get("sunset")),
        )

    @staticmethod
    def _parse_time(val):
        if not val or not val.strip():
            return None
        val = val.strip()
        for fmt in ("%I:%M %p", "%H:%M:%S", "%H:%M"):
            try:
                return datetime.strptime(val, fmt).time()
            except ValueError:
                continue
        return None

    @staticmethod
    def _parse_float(val):
        try:
            return float(val) if val and val.strip() else None
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _parse_int(val):
        try:
            return int(float(val)) if val and val.strip() else None
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _parse_datetime(val):
        if not val or not val.strip():
            return None
        for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                return datetime.strptime(val.strip(), fmt)
            except ValueError:
                continue
        return None
