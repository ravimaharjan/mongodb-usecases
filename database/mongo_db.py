import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient


load_dotenv()

async def get_db():
    password = os.getenv('PASSWORD')
    username = os.getenv('MONGODB_USERNAME')
    db_name = os.getenv('MONGODB_DATABASE')
    host = os.getenv('MONGODB_HOST')

    # Connectionstring format will be different if you are running mongo
    # in localhost. replace it with the format
    # "mongodb://{username}:{password}@localhost:<port>"
    
    connection_uri = f"mongodb+srv://{username}:{password}@{host}/{db_name}"

    try:
        client = AsyncIOMotorClient(connection_uri)
        await client.admin.command('ping')
        print("Connected to MongoDb")

        db = client[db_name]
        return db
    except Exception as e:
        print(e)
        raise(e)
