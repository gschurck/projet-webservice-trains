from typing import List

import pynecone as pc


class TrainClass(pc.Base):
    id: int
    seat_class: str
    available_seats_count: int
    price_flexible: float
    price_not_flexible: float


class Train(pc.Base):
    id: int
    departure_station: str
    arrival_station: str
    departure_date: str
    departure_time: str
    classes: List[TrainClass] = []
