from typing import List, Sequence

from fastapi import APIRouter, Path, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas.schemas import SightseeingModel, SightseeingResponse, SightseeingUpdateModel
from src.repository import sightseeings as repository_sightseeings

router = APIRouter(prefix='/sightseeings', tags=["sightseeings"])


def raise_404_error() -> None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

@router.get("/", response_model=List[SightseeingResponse])
def read_all_sightseeings(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
) -> Sequence[SightseeingResponse]:
    sightseeings = repository_sightseeings.get_all_sightseeings(skip, limit, db)
    return sightseeings

@router.get("/{item_id}", response_model=SightseeingResponse)
def read_sightseeing_by_id(
    item_id: int = Path(..., title="The ID of the sightseeing item to get", ge=1),
    db: Session = Depends(get_db)
) -> SightseeingResponse:
    sightseeing = repository_sightseeings.get_sightseeing_by_id(item_id, db)
    if sightseeing is None:
        raise_404_error()
    return sightseeing

@router.post("/", response_model=SightseeingResponse, status_code=201)
def create_sightseeing(
    body: SightseeingModel,
    db: Session = Depends(get_db)
) -> SightseeingResponse:
    return repository_sightseeings.create_sightseeing(body, db)

@router.patch("/{item_id}", response_model=SightseeingResponse)
def update_sightseeing(
    item_id: int,
    body: SightseeingUpdateModel,
    db: Session = Depends(get_db)
) -> SightseeingResponse:
    sightseeing = repository_sightseeings.update_sightseeing(item_id, body, db)
    if sightseeing is None:
        raise_404_error()
    return sightseeing

@router.delete("/{item_id}", response_model=SightseeingResponse)
def delete_item(item_id: int, db: Session = Depends(get_db)) -> SightseeingResponse:
    sightseeing = repository_sightseeings.delete_sightseeing(item_id, db)
    if sightseeing is None:
        raise_404_error()
    return sightseeing