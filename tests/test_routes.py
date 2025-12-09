# import json

from starlette.testclient import TestClient

def test_routes_crud(client: TestClient) -> None:
    # POST create
    payload = {"name": "Statue of Liberty", "location": "New York", "description": "A gift"}
    resp = client.post("/api/sightseeings/", json=payload)
    assert resp.status_code == 201
    created = resp.json()
    assert created["id"] is not None
    item_id = created["id"]
    assert created["name"] == "Statue of Liberty"
    assert created["location"] == "New York"
    assert created["description"] == "A gift"

    # GET list
    resp = client.get("/api/sightseeings/")
    assert resp.status_code == 200
    data = resp.json()
    assert any(item["id"] == item_id for item in data)

    # GET by id
    resp = client.get(f"/api/sightseeings/{item_id}")
    assert resp.status_code == 200
    obj = resp.json()
    assert obj["name"] == "Statue of Liberty"

    # PATCH update
    patch_payload = {"description": "A gift from France"}
    resp = client.patch(f"/api/sightseeings/{item_id}", json=patch_payload)
    assert resp.status_code == 200
    obj = resp.json()
    assert obj["description"] == "A gift from France"

    # DELETE
    resp = client.delete(f"/api/sightseeings/{item_id}")
    assert resp.status_code == 200
    obj = resp.json()
    assert obj["id"] == item_id

    # GET after delete -> 404
    resp = client.get(f"/api/sightseeings/{item_id}")
    assert resp.status_code == 404