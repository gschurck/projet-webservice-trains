from enum import Enum
from typing import Optional, List

from pydantic.schema import datetime
from sqlalchemy import DateTime, Column
from sqlmodel import Field, SQLModel, Relationship


# TrainStation

class TrainStation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


# Train

class TrainBase(SQLModel):
    departure_station: str
    arrival_station: str
    departure_time: datetime = Field(default=None, sa_column=Column(DateTime))
    arrival_time: datetime = Field(default=None, sa_column=Column(DateTime))


class Train(TrainBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    train_class_seats: List["TrainClassSeats"] = Relationship(back_populates="train",
                                                              sa_relationship_kwargs={"lazy": "subquery"})


class TrainRead(TrainBase):
    id: int


class TrainWithClassSeats(TrainRead):
    train_class_seats: List["TrainClassSeatsRead"]


class TrainUpdate(SQLModel):
    departure_station: Optional[str] = None
    arrival_station: Optional[str] = None
    outbound_time: Optional[datetime] = None
    return_time: Optional[datetime] = None


# TrainClassSeats

# enum seat_class
class SeatClass(str, Enum):
    FIRST = "first"
    BUSINESS = "business"
    STANDARD = "standard"


class TrainClassSeatsBase(SQLModel):
    seat_class: SeatClass
    available_seats_count: int
    train_id: int = Field(default=None, foreign_key="train.id")


class TrainClassSeats(TrainClassSeatsBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    train: Train = Relationship(back_populates="train_class_seats")


class TrainClassSeatsRead(TrainClassSeatsBase):
    id: int
