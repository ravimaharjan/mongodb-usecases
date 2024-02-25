import asyncio
from faker import Faker
from uuid import uuid4
from database.mongo_db import get_db

fake = Faker()


def generate_broker_data():
    broker_data = []
    for i in range(3):
        first_name = fake.first_name()
        data = {
            "broker_id": str(uuid4()),
            "first_name": first_name,
            "last_name": fake.last_name(),
            "email": first_name + "@example.org",
            "phone": fake.phone_number(),
        }

        broker_data.append(data)
    return broker_data

async def run_seed_brokers():
    db = await get_db()

    broker_data = generate_broker_data()
    await db["brokers"].insert_many(broker_data)

if __name__ == "__main__":
    asyncio.run(run_seed_brokers())