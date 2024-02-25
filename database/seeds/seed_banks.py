import asyncio
from faker import Faker
import uuid
import datetime
from database.mongo_db import get_db


def generate_banks_data():
    fake = Faker()
    banks = [
        {
            "name": "JPMorgan Chase",
            "uuid": str(uuid.uuid4()),
            "address": fake.address(),
            "phone": fake.phone_number(),
            "email": fake.email(),
        },
        {
            "name": "Bank of America",
            "uuid": str(uuid.uuid4()),
            "address": fake.address(),
            "phone": fake.phone_number(),
            "email": fake.email(),
        },
        {
            "name": "Citigroup",
            "uuid": str(uuid.uuid4()),
            "address": fake.address(),
            "phone": fake.phone_number(),
            "email": fake.email(),
        },
        {
            "name": "Morgan Stanley",
            "uuid": str(uuid.uuid4()),
            "address": fake.address(),
            "email": fake.email(),
        },
        {
            "name": "Wells Fargo",
            "uuid": str(uuid.uuid4()),
            "address": fake.address(),
            "phone": fake.phone_number(),
            "email": fake.email(),
        }
    ]
    return banks

async def run_seed_banks():
    db = await get_db()
    banks_data = generate_banks_data()
    await db["banks"].insert_many(banks_data)

if __name__ == "__main__":
    asyncio.run(run_seed_banks())