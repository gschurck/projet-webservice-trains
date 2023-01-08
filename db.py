from contextlib import contextmanager
from typing import Type

from pydantic.schema import datetime
from sqlmodel import Session as SQLModelSession, SQLModel, create_engine, select

from models import Train, TrainClassSeats, SeatClass

train_1 = Train(
    departure_station="London",
    arrival_station="Paris",
    departure_time=datetime(2021, 1, 1, 10, 0, 0),
    arrival_time=datetime(2021, 1, 1, 12, 0, 0),
    train_class_seats=[
        TrainClassSeats(seat_class=SeatClass.FIRST, available_seats_count=10),
        TrainClassSeats(seat_class=SeatClass.BUSINESS, available_seats_count=20),
        TrainClassSeats(seat_class=SeatClass.STANDARD, available_seats_count=30),
    ]
)


def delete_all(model: Type[SQLModel]):
    with Session() as session:
        rows = session.exec(select(model)).all()
        for r in rows:
            session.delete(r)
        session.commit()


engine = create_engine("postgresql://postgres:password@db:5432/database")


def init_db():
    SQLModel.metadata.create_all(engine)

    with Session() as session:
        print("session", session)
        delete_all(Train)
        delete_all(TrainClassSeats)
        session.commit()

        session.add(train_1)
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
