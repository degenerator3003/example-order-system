import aio_pika
import json
import os
import asyncio

RABBIT_URL = os.getenv("RABBIT_URL","amqp://guest:guest@rabbit:5672/")

async def publish_message(message: dict, queue_name: str = "orders"):
    print("Connect to RabbitMQ",repr(RABBIT_URL))
    connection = await aio_pika.connect_robust(RABBIT_URL)
    channel = await connection.channel()
    await channel.declare_queue(
        queue_name,
        durable=True,
    )
    body = json.dumps(message).encode()
    await channel.default_exchange.publish(
        aio_pika.Message(body),
        routing_key=queue_name,
    )

    await connection.close()


