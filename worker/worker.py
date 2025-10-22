
import asyncio
import aio_pika
import json
import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.getenv("MONGO_URL","mongodb://mongo:27017/demo")
RABBIT_URL = os.getenv("RABBIT_URL","amqp://guest:guest@rabbit:5672/")


async def handle_message(
    message: aio_pika.IncomingMessage,
    mongo,
):
    async with message.process():
        data = json.loads(message.body)
        print("Processing order:",data)
        inp = {}
        inp["order"]=data
        inp["status"]="done"
        await mongo.processed.insert_one(inp)


async def main():
    mongo = AsyncIOMotorClient(MONGO_URL).get_default_database()
    connection = await aio_pika.connect_robust(RABBIT_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue("orders",durable=True)

    async with queue.iterator() as q:
        async for message in q:
            await hangle_message(message,mongo)


if __name__=="__main__":
    asyncio.run(main())







