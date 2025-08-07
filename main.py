from typing import Optional, Dict, List

from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Sightseeing(BaseModel):
    name: str
    description: Optional[str] = None
    is_visited: Optional[bool] = False


class SightseeingUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_visited: Optional[bool] = None


sightseeings: Dict[int, Sightseeing] = {}
current_id = 1

def raise_404_error() -> None:
    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/")
async def read_root() -> dict:
    return {"message": "Hello, World!"}

@app.get("/sightseeings/", response_model=List[dict])
async def read_items(skip: int = 0, limit: int = 10) -> List[dict]:
    items = list(sightseeings.items())[skip: skip + limit]
    return [{"id": item_id, **item.model_dump()} for item_id, item in items]

@app.get("/sightseeings/{item_id}", response_model=dict)
async def read_item(item_id: int = Path(..., title="The ID of the sightseeing item to get",
                                        ge=1)) -> dict:
    if item_id not in sightseeings:
        raise_404_error()
    return {"id": item_id, **sightseeings[item_id].model_dump()}

@app.post("/sightseeings", response_model=dict, status_code=201)
async def create_item(sightseeing: Sightseeing) -> dict:
    global current_id
    sightseeings[current_id] = sightseeing
    current_id += 1
    return {"id": current_id - 1, **sightseeing.model_dump()}

@app.patch("/sightseeings/{item_id}", response_model=dict)
async def update_item(item_id: int, sightseeing: SightseeingUpdate) -> dict:
    if item_id not in sightseeings:
        raise_404_error()
    stored_item = sightseeings[item_id]
    update_data = sightseeing.model_dump(exclude_unset=True)
    updated_item = stored_item.model_copy(update=update_data)
    sightseeings[item_id] = updated_item
    return {"id": item_id, **updated_item.model_dump()}

@app.delete("/sightseeings/{item_id}", response_model=dict)
async def delete_item(item_id: int) -> dict:
    if item_id not in sightseeings:
        raise_404_error()
    del sightseeings[item_id]
    return {"message": f"Item {item_id} deleted"}