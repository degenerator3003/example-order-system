from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
import os
from rabbit import publish_message

app = FastAPI(title = "NoSQL + RabbitMQ Demo API")

MONGO_URL = os.getenv(
        "MONGO_URL",
        "mongodb://mongo:27017/demo",
    )

mongo = AsyncIOMotorClient(MONGO_URL).get_default_database()

@app.post("/orders")
async def create_order(order: dict):
    result = await mongo.orders.insert_one(order)
    order["_id"] = str(result.inserted_id)
    await publish_message(order)
    return {"status":"queued","order":order}


@app.get("/orders")
async def list_orders():
    cursor = mongo.orders.find()
    orders = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        orders.append(doc)
    return orders



