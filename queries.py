
from datetime import datetime
import asyncio
from database.mongo_db import get_db

async def get_purchase_data(user_id):
    db = await get_db()

    pipeline = [
    {
        "$match": {
            "user_id": user_id
        }
    },
    {
        "$unwind": "$purchase_data"
    },
    {
        "$lookup": {
            "from": "banks",
            "localField": "purchase_data.loan_detail.bank_id",
            "foreignField": "uuid",
            "as": "bank_info"
        }
    },
    {
        "$unwind": "$bank_info"
    },
    {
        "$project": {
            "buyer": {"$concat": ["$first_name", " ", "$last_name"]},
            "buyer_phone": "$phone",
            "buyer_email": "$email",
            "purchase_data": {
                "purchase_id": "$purchase_data.purchase_id",
                "property_id": "$purchase_data.property_id",
                "broker_id": "$purchase_data.broker_id",
                "seller_id": "$purchase_data.seller_id",
                "loan_data": {
                    "loan_amount": "$purchase_data.loan_detail.loan_amount",
                    "interest_rate": "$purchase_data.loan_detail.interest_rate",
                    "bank_name": "$bank_info.name"
                }
            },
        }
    },
    {
        "$group":{
            "_id": "$_id",
            "purchase_data": {
                "$push": "$purchase_data"
            },
            "doc": { "$first": "$$ROOT" }
        }
    },
    {
        "$unset": ["doc.purchase_data"]
    },
      { "$replaceRoot": { 
          "newRoot":{
              "$mergeObjects": [
                    {
                        "purchase_data": "$purchase_data"
                    }, "$doc" 
                ]
            }
        }
    }
    ]
    start_time  = datetime.now()
    result = await db["users_test"].aggregate(pipeline).to_list(length=None)
    end_time = datetime.now()

    # Uncomment to see the result
    # print(result)

    print(f" total time taken {end_time - start_time}")


if __name__ == "__main__":
    test_user_id = "cbfc5b52-a43d-4dbb-b20f-bfcb24bfc19f"
    asyncio.run(get_purchase_data(test_user_id))