from fastapi import FastAPI, HTTPException

app = FastAPI(title="Product Service")

products = {
    1: {"id": 1, "name": "Laptop", "price": 7500000, "stock": 10},
    2: {"id": 2, "name": "Mouse", "price": 150000, "stock": 25},
    3: {"id": 3, "name": "Keyboard", "price": 300000, "stock": 15}
}


@app.get("/")
def root():
    return {"message": "Product Service is running"}


@app.get("/products")
def get_products():
    return list(products.values())


@app.get("/products/{product_id}")
def get_product(product_id: int):
    product = products.get(product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product