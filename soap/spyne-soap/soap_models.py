from spyne import ComplexModel, Unicode, Integer, Float
from spyne import Enum


class CustomModel(ComplexModel):
    name = Unicode


# spyne enum


SeatClass = Enum('first', 'standard', 'business', type_name="SeatClass")


class TrainClass(ComplexModel):
    id = Integer
    seat_class = SeatClass
    available_seats_count = Integer
    price_flexible = Float
    price_not_flexible = Float


class Train(ComplexModel):
    departure_station = Unicode
    arrival_station = Unicode
    departure_date = Unicode
    departure_time = Unicode
    id = Integer
    classes = TrainClass.customize(max_occurs='unbounded')
