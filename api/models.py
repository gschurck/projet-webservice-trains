from datetime import date, time
from enum import Enum
from typing import Optional, List

from sqlalchemy import Column, Date, Time
from sqlmodel import Field, SQLModel, Relationship


# TrainStation

class TrainStation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


# Train

class TrainBase(SQLModel):
    departure_station: str
    arrival_station: str
    departure_date: date = Field(default=None, sa_column=Column(Date))
    departure_time: time = Field(default=None, sa_column=Column(Time))


class Train(TrainBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    train_classes: List["TrainClass"] = Relationship(back_populates="train",
                                                     sa_relationship_kwargs={"lazy": "subquery"})


class TrainRead(TrainBase):
    id: int


class TrainUpdate(SQLModel):
    departure_station: Optional[str] = None
    arrival_station: Optional[str] = None
    departure_date: Optional[date] = None
    departure_time: Optional[time] = None


# TrainClassSeats

# enum seat_class
class SeatClass(str, Enum):
    FIRST = "first"
    BUSINESS = "business"
    STANDARD = "standard"


class TrainClassBase(SQLModel):
    seat_class: SeatClass
    available_seats_count: int = Field(ge=0)
    price_flexible: float = Field(ge=0)
    price_not_flexible: float = Field(ge=0)
    train_id: int = Field(default=None, foreign_key="train.id")


class TrainClass(TrainClassBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    train: Train = Relationship(back_populates="train_classes")


Train.update_forward_refs(TrainClass=TrainClass)


class TrainClassRead(TrainClassBase):
    id: int


class FullTrainClassRead(TrainClassBase):
    id: int
    seat_class: SeatClass
    available_seats_count: int
    price_flexible: float
    price_not_flexible: float


class TrainClassUpdate(SQLModel):
    seat_class: Optional[SeatClass] = None
    available_seats_count: Optional[int] = None


class TrainWithClasses(TrainRead):
    train_classes: List[TrainClassRead]
