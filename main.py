from typing import List
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException
from pydantic.types import UUID1

from models import Gender, Role, User

app = FastAPI()

db: List[User] = [
    User(id=UUID("25ee0a37-ecc3-42d0-9860-950fc4e78e25"), first_name="Dildora", last_name="Raxmatova", middle_name="Baxshilloyevna", gender=Gender.female, roles=[Role.user]),
    User(id=UUID("d61276ab-ef28-4fd7-bda2-6aa19a17de06"), first_name="Ulug'bek", last_name="Hamroyev", middle_name="Maxsudovich", gender=Gender.male, roles=[Role.user, Role.admin])
]

@app.get("/")
def root():
    return {"Hello": "Oybek "}

@app.get("/api/v1/users")
async def fetch_users():
    return db

@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}

@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    print(user_id)
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exists"
    )


# localhost:8000/docs -> automatic genereted swagger
# localhost:8000/redoc -> automatic generated swagger-doc