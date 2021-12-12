from typing import Dict, Optional
from fastapi import FastAPI, Query, status, Body, HTTPException
from pydantic import BaseModel
from pydantic.networks import EmailStr

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
# There are also Path and Body functions like Query. As you know, Path is for path-parameters and body is for request-body.

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

class User(BaseModel):
    username: str
    full_name: Optional[str] = None

@app.put("/items/{item_id}")
async def update_item(
    item_id: int, item: Item, user: User, importance: int = Body(...) # item_id comes from path, item, user and importance come from request-body
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results
# for this endpoint request body may be
# {
#   "item": {
#       "name": "liboy",
#       "description": "any description",
#       "price": 11.11
#       "tax": 11.1
#   },
#   "user": {
#       "username": "Oybek",
#       "full_name": "Oybek Makhsudov"
#   }
#   "importance": 1111
# }

# Look at the example shown below
@app.post("/index-weights/")
async def create_index_weights(weights: Dict[int, float]):
    return weights

# As we know, JSON only supports string key-values. But Pydantic and Python's "typing" module have automatic data conversion.
# So even though you reciev str key-value pairs Pydantic converts it automaticly (for example, to int-float key-values)

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None

class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn):
    return user
# Here we are returning user which is in type UserIn. However, we shown UserOut-type in response_model. So our response will be sent in UserOut type

@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}

items = {"foo": "Go Foo go"}

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found") # detail could also be a dist, a list, etc. Not only str.
    return {"item": items[item_id]}