from typing import Optional
from fastapi import FastAPI

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/") # "/items/" is path
async def read_item(skip: int = 0, limit: int = 10): # skip: int = 0 -> int is type of skip and 0 is a default value for skip
    return fake_items_db[skip : skip+limit]

# http://127.0.0.1:8000/items/?skip=0&limit=10 -> "/items/" is path. The part after "?" is query parameters separated by "&"

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None): # q will be not required
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}