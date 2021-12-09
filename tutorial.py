from typing import Optional
from fastapi import FastAPI, Query

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

@app.get("/items-q/")
async def read_items(q: Optional[str] = Query(None, max_length=50)): # q will be Optional string, its max_length will be 50 chars and its default value will be None
    result = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        result.update({"q": q})
    
    return result

# q: str = Query(..., max_length=19) -> q will be required. "..." is a special value in Python
# q: Optional[List[str]] = Query(None) -> q will be able to take many values
# Example URL: http://localhost:8000/items/?q=foo&q=bar
# The response to this query would be { "q": [ "foo", "bar" ] }
# q: List[str] = Query(["foo", "bar"]) -> ["foo", "bar"] is default value for q
# q: list = Query([]) -> also valid
