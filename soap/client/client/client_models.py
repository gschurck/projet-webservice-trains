from typing import List

from pydantic import BaseModel


class TrainClass(BaseModel):
    seat_class: str
    available_seats_count: int


class Train(BaseModel):
    id: int
    departure_station: str
    arrival_station: str
    departure_date: str
    departure_time: str
    classes: List[TrainClass] = []
