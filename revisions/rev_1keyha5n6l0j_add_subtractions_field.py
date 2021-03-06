"""
Add subtractions field

Revision ID: 1keyha5n6l0j
Date: 2022-06-09 22:04:28.890559

"""
from asyncio import gather

import arrow
from motor.motor_asyncio import (
    AsyncIOMotorClientSession,
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)

# Revision identifiers.
from pymongo import UpdateOne

name = "Add subtractions field"
created_at = arrow.get("2022-06-09 22:04:28.890559")
revision_id = "1keyha5n6l0j"


async def upgrade(motor_db: AsyncIOMotorDatabase, session: AsyncIOMotorClientSession):
    for collection in [motor_db.analyses, motor_db.samples]:
        updates = []

        async for document in collection.find({"subtraction": {"$exists": True}}):
            try:
                subtractions = [document["subtraction"]["id"]]
            except TypeError:
                subtractions = list()

            update = UpdateOne(
                {"_id": document["_id"]},
                {"$set": {"subtractions": subtractions}, "$unset": {"subtraction": ""}},
            )

            updates.append(update)

        if updates:
            await collection.bulk_write(updates)


async def test_upgrade(mongo, snapshot):
    await gather(
        mongo.samples.insert_many(
            [
                {"_id": "foo", "subtraction": {"id": "prunus"}},
                {"_id": "bar", "subtraction": {"id": "malus"}},
                {"_id": "baz", "subtraction": None},
            ]
        ),
        mongo.analyses.insert_many(
            [
                {"_id": "foo", "subtraction": {"id": "prunus"}},
                {"_id": "bar", "subtraction": {"id": "malus"}},
                {"_id": "baz", "subtraction": None},
            ]
        ),
    )

    async with await mongo.client.start_session() as session:
        async with session.start_transaction():
            await upgrade(mongo, session)

    assert await mongo.analyses.find().to_list(None) == snapshot(name="analyses")
    assert await mongo.samples.find().to_list(None) == snapshot(name="samples")
