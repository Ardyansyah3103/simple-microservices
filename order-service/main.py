from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI(title="Order Service")

USER_SERVICE_URL = "http://localhost:8001"
PRODUCT_SERVICE_URL = "http://localhost:8002"

orders = []

class OrderRequest(BaseModel):
    user_id: int
    product_id: int
    quantity: int

@app.get("/")
def root():
    return {"message": "Order Service is running"}

@app.get("/orders")
def get_orders():
    return orders

@app.post("/orders")
def create_order(order: OrderRequest):
    # validasi user
    user_response = requests.get(f"{USER_SERVICE_URL}/users/{order.user_id}")
    if user_response.status_code != 200:
        raise HTTPException(status_code=400, detail="User not found")
    
    # validasi produk
    product_response = requests.get(f"{PRODUCT_SERVICE_URL}/products/{order.product_id}")
    if product_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Product not found")
    
    user = user_response.json()
    product = product_response.json()

    # validasi stok
    if order.quantity > product["stock"]:
        raise HTTPException(status_code=400, detail="Not enough product stock")
    
    # buat order
    total_price = product["price"] * order.quantity

    new_order = {
        "id": len(orders) + 1,
        "user": user,
        "product": product,
        "quantity": order.quantity,
        "total_price": total_price,
        "status": "created"
    }

    orders.append(new_order)
    return {
        "message": "Order created successfully",
        "order": new_order
    }