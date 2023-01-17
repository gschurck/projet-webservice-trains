from typing import List

from pydantic import BaseModel


class TrainClass(BaseModel):
    seat_class: str
    available_seats_count: int


class Train(BaseModel):
    departure_station: str
    arrival_station: str
    departure_time: str
    id: int
    classes: List[TrainClass] = []
