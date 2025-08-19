from typing import List, Sequence

from fastapi import APIRouter, Path, HTTPException, Depends, status, Query

from src.dependency_injection.di import get_sightseeing_repository
from src.schemas.schemas import SightseeingModel, SightseeingResponse, SightseeingUpdateModel
from src.repository.sightseeings_repository import SightseeingRepository

router = APIRouter(prefix='/sightseeings', tags=["sightseeings"])


def raise_404_error() -> None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

@router.get("/", response_model=List[SightseeingResponse])
def read_all_sightseeings(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    db: SightseeingRepository = Depends(get_sightseeing_repository)
) -> Sequence[SightseeingResponse]:
    sightseeings = db.get_all_sightseeings(skip, limit)
    return sightseeings

@router.get("/{item_id}", response_model=SightseeingResponse)
def read_sightseeing_by_id(
    item_id: int = Path(..., title="The ID of the sightseeing item to get", ge=1),
    db: SightseeingRepository = Depends(get_sightseeing_repository)
) -> SightseeingResponse:
    sightseeing = db.get_sightseeing_by_id(item_id)
    if sightseeing is None:
        raise_404_error()
    return sightseeing

@router.post("/", response_model=SightseeingResponse, status_code=201)
def create_sightseeing(
    body: SightseeingModel,
    db: SightseeingRepository = Depends(get_sightseeing_repository)
) -> SightseeingResponse:
    return db.create_sightseeing(body)

@router.patch("/{item_id}", response_model=SightseeingResponse)
def update_sightseeing(
    item_id: int,
    body: SightseeingUpdateModel,
    db: SightseeingRepository = Depends(get_sightseeing_repository)
) -> SightseeingResponse:
    sightseeing = db.update_sightseeing(item_id, body)
    if sightseeing is None:
        raise_404_error()
    return sightseeing

@router.delete("/{item_id}", response_model=SightseeingResponse)
def delete_item(item_id: int, db: SightseeingRepository = Depends(get_sightseeing_repository)) -> SightseeingResponse:
    sightseeing = db.delete_sightseeing(item_id)
    if sightseeing is None:
        raise_404_error()
    return sightseeing