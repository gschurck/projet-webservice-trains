from typing import Optional, List

from db import Train, TrainClass, get_session, engine
from fastapi import APIRouter, HTTPException, Depends
from fastapi_filter import FilterDepends, with_prefix
from fastapi_filter.contrib.sqlalchemy import Filter
from models import TrainRead, TrainWithClasses, TrainUpdate, FullTrainClassRead
from sqlmodel import Session, select

from routes.trains_subroutes import train_class_routes

router = APIRouter(
    prefix="/trains", tags=["trains"],
)


class TrainClassFilter(Filter):
    seat_class__in: Optional[List[str]]

    class Constants(Filter.Constants):
        model = TrainClass


class TrainFilter(Filter):
    departure_station: Optional[str]
    departure_station__ilike: Optional[str]
    departure_station__like: Optional[str]
    search: Optional[str]
    train_class_seats: Optional[TrainClassFilter] = FilterDepends(with_prefix("train", TrainClassFilter))

    # available_seats_count__gt: Optional[int]

    class Constants(Filter.Constants):
        model = Train
        search_model_fields = ["departure_station"]


@router.get("", response_model=List[TrainRead])
async def get_trains(train_filter: TrainFilter = FilterDepends(TrainFilter), db: Session = Depends(get_session)):
    query = select(Train).distinct(Train.id)
    query = train_filter.filter(query)
    return db.exec(query).all()


@router.get("/{train_id}", response_model=TrainWithClasses)
async def get_train(train_id: int, db: Session = Depends(get_session)):
    train = db.get(Train, train_id)
    if not train:
        raise HTTPException(status_code=404, detail="Train not found")
    return train


@router.patch("/{train_id}", response_model=TrainRead)
def update_hero(train_id: int, train: TrainUpdate):
    with Session(engine) as session:
        db_train = session.get(Train, train_id)
        if not db_train:
            raise HTTPException(status_code=404, detail="Train not found")
        hero_data = train.dict(exclude_unset=True)
        for key, value in hero_data.items():
            setattr(db_train, key, value)
        session.add(db_train)
        session.commit()
        session.refresh(db_train)
        return db_train


@router.get("/{train_id}/classes", response_model=List[FullTrainClassRead])
def get_train_classes(train_id: int, db: Session = Depends(get_session)):
    train_classes = db.exec(select(TrainClass).where(TrainClass.train_id == train_id)).all()
    return train_classes


router.include_router(train_class_routes.router, tags=["trains"])
