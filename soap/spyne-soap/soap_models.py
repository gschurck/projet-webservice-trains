from spyne import ComplexModel, Unicode, Integer
from spyne import Enum


class CustomModel(ComplexModel):
    name = Unicode


# spyne enum


SeatClass = Enum('first', 'standard', 'business', type_name="SeatClass")


class TrainClass(ComplexModel):
    id = Integer
    seat_class = SeatClass
    available_seats_count = Integer


class Train(ComplexModel):
    departure_station = Unicode
    arrival_station = Unicode
    departure_time = Unicode
    id = Integer
    # train_classes = TrainClass.customize(max_occurs='unbounded')
