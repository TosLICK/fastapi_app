from typing import List

from sqlalchemy.orm import Session

from src.database.models import Sightseeing
from src.schemas.schemas import SightseeingModel, SightseeingUpdateModel


def get_all_sightseeings(skip: int, limit: int, db: Session) -> List[Sightseeing]:
    return db.query(Sightseeing).offset(skip).limit(limit).all()


def get_sightseeing_by_id(item_id: int, db: Session) -> Sightseeing:
    return db.query(Sightseeing).filter(Sightseeing.id == item_id).first()


def create_sightseeing(body: SightseeingModel, db: Session) -> Sightseeing:
    sightseeing = Sightseeing(name=body.name, location=body.location, description=body.description)
    db.add(sightseeing)
    db.commit()
    db.refresh(sightseeing)
    return sightseeing


def update_sightseeing(item_id: int, body: SightseeingUpdateModel, db: Session) -> Sightseeing | None:
    sightseeing = db.query(Sightseeing).filter(Sightseeing.id == item_id).first()
    if sightseeing is None:
        return None
    update_data = body.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(sightseeing, key, value)
    db.commit()
    db.refresh(sightseeing)
    return sightseeing


def delete_sightseeing(item_id: int, db: Session) -> Sightseeing | None:
    sightseeing = db.query(Sightseeing).filter(Sightseeing.id == item_id).first()
    if sightseeing:
        db.delete(sightseeing)
        db.commit()
    return sightseeing
