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


class Train(TrainBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    train_classes: List["TrainClass"] = Relationship(back_populates="train",
                                                     sa_relationship_kwargs={"lazy": "subquery"})


class TrainRead(TrainBase):
    id: int


class TrainUpdate(SQLModel):
    departure_station: Optional[str] = None
    arrival_station: Optional[str] = None
    departure_time: Optional[datetime] = None


# TrainClassSeats

# enum seat_class
class SeatClass(str, Enum):
    FIRST = "first"
    BUSINESS = "business"
    STANDARD = "standard"


class TrainClassBase(SQLModel):
    seat_class: SeatClass
    available_seats_count: int = Field(ge=0)
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


class TrainClassUpdate(SQLModel):
    seat_class: Optional[SeatClass] = None
    available_seats_count: Optional[int] = None


class TrainWithClasses(TrainRead):
    train_classes: List[TrainClassRead]
