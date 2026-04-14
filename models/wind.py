import enum

from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship

from models.base import Base


class WindDirectionEnum(enum.Enum):
    N = "N"
    NNE = "NNE"
    NE = "NE"
    ENE = "ENE"
    E = "E"
    ESE = "ESE"
    SE = "SE"
    SSE = "SSE"
    S = "S"
    SSW = "SSW"
    SW = "SW"
    WSW = "WSW"
    W = "W"
    WNW = "WNW"
    NW = "NW"
    NNW = "NNW"

    @classmethod
    def from_string(cls, value):
        if value is None:
            return None
        try:
            return cls(value.strip().upper())
        except (ValueError, AttributeError):
            return None


class WindData(Base):
    __tablename__ = "wind_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    weather_id = Column(
        Integer,
        ForeignKey("weather_data.id"),
        nullable=False,
        unique=True,
    )

    wind_degree = Column(Integer)
    wind_kph = Column(Float)
    wind_mph = Column(Float)
    wind_direction = Column(String(10))
    gust_mph = Column(Float)
    gust_kph = Column(Float)

    should_go_outside = Column(Boolean, default=True, server_default="1")

    weather = relationship("WeatherData", back_populates="wind")

    @property
    def direction_enum(self):
        return WindDirectionEnum.from_string(self.wind_direction)

    def __repr__(self):
        return (
            f"<Wind weather_id={self.weather_id} "
            f"kph={self.wind_kph} dir={self.wind_direction} "
            f"go_outside={self.should_go_outside}>"
        )
