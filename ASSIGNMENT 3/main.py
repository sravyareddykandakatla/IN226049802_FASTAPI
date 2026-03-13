from fastapi import FastAPI, HTTPException

app = FastAPI()

# Initial Product List
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 599, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Keyboard", "price": 999, "category": "Electronics", "in_stock": True},
    {"id": 3, "name": "Notebook", "price": 50, "category": "Stationery", "in_stock": False},
    {"id": 4, "name": "Pen", "price": 20, "category": "Stationery", "in_stock": True}
]

# GET all products
@app.get("/products")
def get_products():
    return products


# PRODUCT AUDIT (must come before /products/{product_id})
@app.get("/products/audit")
def product_audit():

    in_stock_products = [p for p in products if p["in_stock"]]
    out_stock_products = [p for p in products if not p["in_stock"]]

    most_expensive = max(products, key=lambda x: x["price"])

    return {
        "total_products": len(products),
        "in_stock_count": len(in_stock_products),
        "out_of_stock_products": [p["name"] for p in out_stock_products],
        "most_expensive_product": most_expensive
    }


# GET product by ID
@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")


# ADD product
@app.post("/products")
def add_product(product: dict):
    product["id"] = len(products) + 1
    products.append(product)
    return {"message": "Product added successfully", "product": product}


# UPDATE product
@app.put("/products/{product_id}")
def update_product(product_id: int, price: int = None, in_stock: bool = None):

    for product in products:
        if product["id"] == product_id:

            if price is not None:
                product["price"] = price

            if in_stock is not None:
                product["in_stock"] = in_stock

            return {"message": "Product updated", "product": product}

    raise HTTPException(status_code=404, detail="Product not found")


# DELETE product
@app.delete("/products/{product_id}")
def delete_product(product_id: int):

    for product in products:
        if product["id"] == product_id:
            products.remove(product)
            return {"message": "Product deleted"}

    raise HTTPException(status_code=404, detail="Product not found")
