"""
Rename username to user_id

Revision ID: mujt2zxouf9p
Date: 2022-06-08 16:49:51.012975

"""
import arrow
from motor.motor_asyncio import AsyncIOMotorClientSession, AsyncIOMotorDatabase

# Revision identifiers.
name = "Rename username to user_id"
created_at = arrow.get("2022-06-08 16:49:51.012975").naive
revision_id = "mujt2zxouf9p"


async def upgrade(motor_db: AsyncIOMotorDatabase, session: AsyncIOMotorClientSession):
    await motor_db.examples.update_many(
        {"username": {"$exists": True}},
        {"$rename": {"username": "user_id"}},
        session=session,
    )
