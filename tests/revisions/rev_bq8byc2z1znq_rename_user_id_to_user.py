"""
Rename user_id to user

Revision ID: bq8byc2z1znq
Date: 2022-06-08 16:49:59.209131

"""
import arrow
from motor.motor_asyncio import AsyncIOMotorClientSession, AsyncIOMotorDatabase

# Revision identifiers.
name = "Rename user_id to user"
created_at = arrow.get("2022-06-08 16:49:59.209131").naive
revision_id = "bq8byc2z1znq"


async def upgrade(motor_db: AsyncIOMotorDatabase, session: AsyncIOMotorClientSession):
    await motor_db.examples.update_many(
        {"user_id": {"$exists": True}},
        {"$rename": {"user_id": "user"}},
        session=session,
    )
