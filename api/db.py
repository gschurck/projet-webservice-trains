from contextlib import contextmanager
from datetime import date, time
from typing import Type

from sqlmodel import Session as SQLModelSession, SQLModel, create_engine, select

from models import Train, TrainClass, SeatClass

train_1 = Train(
    departure_station="London",
    arrival_station="Paris",
    departure_date=date(2023, 1, 1),
    departure_time=time(10, 0),
    train_classes=[
        TrainClass(seat_class=SeatClass.FIRST, available_seats_count=10, price_flexible=50.0,
                   price_not_flexible=40.0),
        TrainClass(seat_class=SeatClass.BUSINESS, available_seats_count=20, price_flexible=100.0,
                   price_not_flexible=80.0),
        TrainClass(seat_class=SeatClass.STANDARD, available_seats_count=30, price_flexible=70.0,
                   price_not_flexible=50.0, ),
    ],
)
train_4 = Train(
    departure_station="London",
    arrival_station="Paris",
    departure_date=date(2023, 1, 1),
    departure_time=time(12, 0),
    train_classes=[
        TrainClass(seat_class=SeatClass.FIRST, available_seats_count=0, price_flexible=50.0,
                   price_not_flexible=40.0),
        TrainClass(seat_class=SeatClass.BUSINESS, available_seats_count=20, price_flexible=100.0,
                   price_not_flexible=80.0),
        TrainClass(seat_class=SeatClass.STANDARD, available_seats_count=30, price_flexible=70.0,
                   price_not_flexible=50.0, ),
    ],
)
train_2 = Train(
    departure_station="Paris",
    arrival_station="Nantes",
    departure_date=date(2023, 2, 2),
    departure_time=time(12, 0),
    train_classes=[
        TrainClass(seat_class=SeatClass.FIRST, available_seats_count=2, price_flexible=40.0,
                   price_not_flexible=30.0),
        TrainClass(seat_class=SeatClass.BUSINESS, available_seats_count=2, price_flexible=80.0,
                   price_not_flexible=60.0),
        TrainClass(seat_class=SeatClass.STANDARD, available_seats_count=2, price_flexible=60.0,
                   price_not_flexible=40.0, ),
    ],
)
train_3 = Train(
    departure_station="Paris",
    arrival_station="Nantes",
    departure_date=date(2023, 2, 2),
    departure_time=time(16, 0),
    train_classes=[
        TrainClass(seat_class=SeatClass.FIRST, available_seats_count=2, price_flexible=50.0,
                   price_not_flexible=40.0),
        TrainClass(seat_class=SeatClass.BUSINESS, available_seats_count=2, price_flexible=100.0,
                   price_not_flexible=80.0),
        TrainClass(seat_class=SeatClass.STANDARD, available_seats_count=2, price_flexible=70.0,
                   price_not_flexible=50.0, ),
    ],
)


def delete_all(model: Type[SQLModel]):
    with Session() as session:
        rows = session.exec(select(model)).all()
        for r in rows:
            session.delete(r)
        session.commit()


engine = create_engine("postgresql://postgres:password@api-db:5432/database")


def init_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    with Session() as session:
        session.add(train_1)
        session.add(train_2)
        session.add(train_3)
        session.add(train_4)

        session.commit()
        print("Done")
        session.close()


@contextmanager
def Session():
    session = SQLModelSession(engine)
    try:
        yield session
    finally:
        session.close()


def get_session():
    with Session() as session:
        yield session
