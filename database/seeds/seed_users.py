import asyncio
import random
from faker import Faker
from uuid import uuid4
from database.mongo_db import get_db

fake = Faker()

# For simplicity, broker_list and bank_list are hard coded. These values
# are taken from the Database itself. If you want, you can replace it with
# code to read ids from the MongoDB

broker_list = [
    "610ab4ff-67c6-4225-b48a-3f53a3262f22",
    "b964a9d6-705b-4004-b03e-31f870a84f2b",
    "99aa582e-904f-4ef4-a117-8f76a3fc76f2",
    "af09cbd1-795e-402d-9ef3-ad967c9f0401",
    "5736edf0-1b6c-4db2-99bc-17f012aa7e25",
    "f452f6db-ac2d-4560-909d-3684c8d57d3f",
    "05423933-b9f3-4d33-836c-6ef71a47d4ef",
    "1868be07-80ba-481b-a3ca-72a5ce278ec6",
    "7ecdf170-6a35-4370-b601-50a54c0d6123",
    "b5589d57-0577-47e7-8f78-1606839ce39c"
]

bank_list = [
    "90a56685-4dc6-4529-93dd-db2cae97f95f",
    "b8ba45cf-c5e5-4c78-a7ad-7945702b29ee",
    "1d1dfa36-5111-4b6f-af79-b482b3d885b6", 
    "1b48e796-d2fe-43e9-8455-5c47eb7ffcc3",
    "53579c6a-08c2-4e91-884f-20e720ce9135",
    "364b203a-751e-4594-911c-95cdb5ca5573"
]


def generate_purchase_data(count):
    purchase_data = []
    for i in range(count):
        data = {
            "purchase_id": str(uuid4()),
            "purchase_date": fake.date_time_between(start_date="-5y", end_date="now"),
            "purchase_bill_id": str(uuid4()),
            "property_id": str(uuid4()),
            "property_type": "land",
            "property_address": fake.address(),
            "propery_area_size": random.choice([4,5,6,7,8,9,10]),
            "seller_id": str(uuid4()),
            "broker_id": random.choice(broker_list),
            "bank_id": random.choice(bank_list),
            "broker_company_id": "",
            "loan_detail": {
                "bank_id": random.choice(bank_list),
                "loan_amount": random.randrange(100000, 800000),
                "loan_term": random.randrange(3, 10),
                "interest_rate": 3.5,
            }
        }
        purchase_data.append(data)
    return purchase_data

def generate_users_data(users_count):
    users_data = []
    for i in range(users_count):
        count = random.choice([2, 3, 4, 5])
        property_purchase_data = generate_purchase_data(count)
        first_name = fake.first_name()
        data = {
            "user_id": str(uuid4()),
            "first_name": first_name,
            "last_name": fake.last_name(),
            "email": first_name + "@example.org",
            "phone": fake.phone_number(),
            "address": fake.address(),
            "dob": fake.date_time(),
            "purchase_data": property_purchase_data, 
        }
        users_data.append(data)
    return users_data

async def run_seed_users(users_count):
    db = await get_db()
    users_data = generate_users_data(users_count)
    await db["users"].insert_many(users_data)

if __name__ == "__main__":
    users_count = 100
    asyncio.run(run_seed_users(users_count))



