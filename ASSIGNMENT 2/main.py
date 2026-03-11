from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()

# Sample product database
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 500, "stock": 10},
    {"id": 2, "name": "Keyboard", "price": 800, "stock": 5},
    {"id": 3, "name": "Monitor", "price": 7000, "stock": 0},
    {"id": 4, "name": "USB Hub", "price": 450, "stock": 15},
]

feedback_list = []

# ---------------------------
# Q1: Filter products
# ---------------------------
@app.get("/products/filter")
def filter_products(
    min_price: int = Query(None, description="Minimum price"),
    max_price: int = Query(None, description="Maximum price")
):
    result = products

    if min_price is not None:
        result = [p for p in result if p["price"] >= min_price]

    if max_price is not None:
        result = [p for p in result if p["price"] <= max_price]

    return result


# ---------------------------
# Q2: Get product price
# ---------------------------
@app.get("/products/{product_id}/price")
def get_product_price(product_id: int):
    for p in products:
        if p["id"] == product_id:
            return {"name": p["name"], "price": p["price"]}

    raise HTTPException(status_code=404, detail="Product not found")


# ---------------------------
# Q3: Feedback API
# ---------------------------
class Feedback(BaseModel):
    name: str
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None


@app.post("/feedback")
def submit_feedback(feedback: Feedback):
    feedback_list.append(feedback)
    return {"message": "Feedback submitted", "data": feedback}


# ---------------------------
# Q4: Product summary
# ---------------------------
@app.get("/products/summary")
def product_summary():
    prices = [p["price"] for p in products]

    return {
        "total_products": len(products),
        "average_price": sum(prices) / len(prices),
        "most_expensive": max(products, key=lambda x: x["price"]),
        "cheapest": min(products, key=lambda x: x["price"]),
        "in_stock": len([p for p in products if p["stock"] > 0])
    }


# ---------------------------
# Q5: Bulk orders
# ---------------------------
class OrderItem(BaseModel):
    product_id: int
    quantity: int


class BulkOrder(BaseModel):
    orders: List[OrderItem]


@app.post("/orders/bulk")
def bulk_orders(order: BulkOrder):
    confirmed = []
    failed = []
    total = 0

    for item in order.orders:
        product = next((p for p in products if p["id"] == item.product_id), None)

        if not product or product["stock"] == 0:
            failed.append(item)
        else:
            cost = product["price"] * item.quantity
            total += cost
            confirmed.append({
                "product": product["name"],
                "quantity": item.quantity,
                "cost": cost
            })

    return {
        "confirmed": confirmed,
        "failed": failed,
        "grand_total": total
    }
