from typing import List

from sqlalchemy.orm import Session

from src.database.models import Sightseeing
from src.schemas.schemas import SightseeingModel, SightseeingUpdateModel

class SightseeingRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all_sightseeings(self, skip: int, limit: int) -> List[Sightseeing]:
        return self.session.query(Sightseeing).offset(skip).limit(limit).all()

    def get_sightseeing_by_id(self, item_id: int) -> Sightseeing | None:
        return self.session.query(Sightseeing).filter(Sightseeing.id == item_id).first()

    def create_sightseeing(self, body: SightseeingModel) -> Sightseeing:
        sightseeing = Sightseeing(name=body.name, location=body.location, description=body.description)
        self.session.add(sightseeing)
        self.session.commit()
        self.session.refresh(sightseeing)
        return sightseeing

    def update_sightseeing(self, item_id: int, body: SightseeingUpdateModel) -> Sightseeing | None:
        sightseeing = self.session.query(Sightseeing).filter(Sightseeing.id == item_id).first()
        if sightseeing is None:
            return None
        update_data = body.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(sightseeing, key, value)
        self.session.commit()
        self.session.refresh(sightseeing)
        return sightseeing

    def delete_sightseeing(self, item_id: int) -> Sightseeing | None:
        sightseeing = self.session.query(Sightseeing).filter(Sightseeing.id == item_id).first()
        if sightseeing:
            self.session.delete(sightseeing)
            self.session.commit()
        return sightseeing
