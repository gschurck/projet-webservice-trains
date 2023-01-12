from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from db import get_session
from models import TrainClassRead, TrainClass, TrainClassUpdate

router = APIRouter(
    prefix="/class",
)


@router.get("/{train_class_id}", response_model=TrainClassRead)
async def get_train_class(train_class_id: int, db: Session = Depends(get_session)):
    train_class = db.get(TrainClass, train_class_id)
    if not train_class:
        raise HTTPException(status_code=404, detail="Train class not found")
    return train_class


@router.patch("/{train_class_id}", response_model=TrainClassRead)
async def update_train_class(train_class_id: int, train_class: TrainClassUpdate, db: Session = Depends(get_session)):
    db_train_class = db.get(TrainClass, train_class_id)
    if not db_train_class:
        raise HTTPException(status_code=404, detail="Train class not found")
    train_class_data = train_class.dict(exclude_unset=True)
    for key, value in train_class_data.items():
        setattr(db_train_class, key, value)
    db.add(db_train_class)
    db.commit()
    db.refresh(db_train_class)
    return db_train_class
