from fastapi import FastAPI, HTTPException

app = FastAPI(title="User Service")

users = {
    1: {"id": 1, "name": "Ardyan", "email": "ardyan@example.com"},
    2: {"id": 2, "name": "Budi", "email": "budi@example.com"}
}


@app.get("/")
def root():
    return {"message": "User Service is running"}


@app.get("/users")
def get_users():
    return list(users.values())


@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = users.get(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user