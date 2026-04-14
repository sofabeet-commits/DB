from sqlalchemy import Column, Integer, String, Float, DateTime, Time

from models.base import Base


class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, autoincrement=True)

    country = Column(String(255), nullable=False)
    location_name = Column(String(255))

    last_updated = Column(DateTime)

    sunrise = Column(Time)
    sunset = Column(Time)

    latitude = Column(Float)
    longitude = Column(Float)
    timezone = Column(String(100))

    temperature_celsius = Column(Float)
    condition_text = Column(String(255))
    humidity = Column(Integer)
    pressure_mb = Column(Float)
    visibility_km = Column(Float)

    wind_degree = Column(Integer)
    wind_kph = Column(Float)
    wind_direction = Column(String(10))
    wind_mph = Column(Float)
    gust_mph = Column(Float)
    gust_kph = Column(Float)

    def __repr__(self):
        return f"<Weather {self.country}/{self.location_name} {self.last_updated}>"
