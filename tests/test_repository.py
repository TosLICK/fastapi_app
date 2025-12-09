import pytest
from sqlalchemy.exc import IntegrityError

from src.repository.sightseeings_repository import SightseeingRepository
from src.schemas.schemas import SightseeingModel, SightseeingUpdateModel


def test_repository_crud(repo: SightseeingRepository) -> None:
    # Create
    payload = SightseeingModel(name="Eiffel Tower", location="Paris", description="Famous tower")
    created = repo.create_sightseeing(payload)
    assert created.id is not None
    assert created.name == "Eiffel Tower"
    assert created.location == "Paris"
    assert created.description == "Famous tower"

    # Get by id
    fetched = repo.get_sightseeing_by_id(created.id)
    assert fetched is not None
    assert fetched.id == created.id
    assert fetched.name == "Eiffel Tower"
    assert fetched.location == "Paris"
    assert fetched.description == "Famous tower"

    # Get all
    all_items = repo.get_all_sightseeings(skip=0, limit=10)
    assert any(item.id == created.id for item in all_items)

    # Update
    update = SightseeingUpdateModel(name="La Tour Eiffel")
    updated = repo.update_sightseeing(created.id, update)
    assert updated is not None
    assert updated.name == "La Tour Eiffel"

    # Delete
    deleted = repo.delete_sightseeing(created.id)
    assert deleted is not None
    # ensure it's gone
    assert repo.get_sightseeing_by_id(created.id) is None


def test_update_nonexistent_returns_none(repo: SightseeingRepository) -> None:
    upd = SightseeingUpdateModel(description="no such item")
    assert repo.update_sightseeing(9999, upd) is None


def test_delete_nonexistent_returns_none(repo: SightseeingRepository) -> None:
    assert repo.delete_sightseeing(9999) is None


def test_get_all_pagination(repo: SightseeingRepository) -> None:
    # create several items and verify skip/limit
    for i in range(3):
        m = SightseeingModel(name=f"name{i}", location="loc", description=None)
        repo.create_sightseeing(m)

    objs = repo.get_all_sightseeings(skip=1, limit=1)
    assert len(objs) == 1
    assert objs[0].name == "name1"


def test_unique_name_constraint(repo: SightseeingRepository) -> None:
    m = SightseeingModel(name="unique_name", location="loc", description=None)
    repo.create_sightseeing(m)
    # Creating another with the same unique name should raise an integrity error
    with pytest.raises(IntegrityError):
        repo.create_sightseeing(m)