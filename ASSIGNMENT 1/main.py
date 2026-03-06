from fastapi import FastAPI

app = FastAPI()

# Sample product database
products = [
    {"id": 1, "name": "Wireless Mouse", "category": "Electronics", "price": 500, "in_stock": True},
    {"id": 2, "name": "Laptop", "category": "Electronics", "price": 50000, "in_stock": True},
    {"id": 3, "name": "Notebook", "category": "Stationery", "price": 50, "in_stock": True},
    {"id": 4, "name": "Pen", "category": "Stationery", "price": 20, "in_stock": False},
    {"id": 5, "name": "Headphones", "category": "Electronics", "price": 1500, "in_stock": True},
    {"id": 6, "name": "Keyboard", "category": "Electronics", "price": 800, "in_stock": False},
    {"id": 7, "name": "Book", "category": "Education", "price": 300, "in_stock": True},
]


# Q1 — Get all products
@app.get("/products")
def get_products():
    return {
        "products": products,
        "total": len(products)
    }


# Q2 — Get products by category
@app.get("/products/category/{category}")
def get_by_category(category: str):
    result = []

    for p in products:
        if p["category"].lower() == category.lower():
            result.append(p)

    return {"products": result}


# Q3 — Get products in stock
@app.get("/products/instock")
def in_stock_products():
    result = []

    for p in products:
        if p["in_stock"]:
            result.append(p)

    return {"products": result}


# Q4 — Store summary
@app.get("/store/summary")
def store_summary():
    total_products = len(products)

    in_stock = 0
    out_stock = 0

    for p in products:
        if p["in_stock"]:
            in_stock += 1
        else:
            out_stock += 1

    return {
        "total_products": total_products,
        "in_stock_products": in_stock,
        "out_of_stock_products": out_stock
    }


# Q5 — Search product
@app.get("/products/search/{keyword}")
def search_product(keyword: str):
    result = []

    for p in products:
        if keyword.lower() in p["name"].lower():
            result.append(p)

    return {"products": result}
