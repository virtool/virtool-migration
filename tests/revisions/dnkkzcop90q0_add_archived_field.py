"""
Add archived field

Revision ID: dnkkzcop90q0
Date: 2022-06-08 16:49:52.725392

"""
import arrow
from motor.motor_asyncio import AsyncIOMotorClientSession, AsyncIOMotorDatabase

# Revision identifiers.
name = "Add archived field"
created_at = arrow.get("2022-06-08 16:49:52.725392").naive
revision_id = "dnkkzcop90q0"


async def upgrade(motor_db: AsyncIOMotorDatabase, session: AsyncIOMotorClientSession):
    await motor_db.examples.update_many(
        {"archived": {"$exists": False}}, {"$set": {"archived": False}}, session=session
    )
