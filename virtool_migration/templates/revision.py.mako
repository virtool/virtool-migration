"""
${name}

Revision ID: ${revision_id}
Date: ${created_at}

"""
import arrow
from motor.motor_asyncio import AsyncIOMotorClientSession, AsyncIOMotorDatabase

# Revision identifiers.
name = "${name}"
created_at = arrow.get("${created_at}")
revision_id = "${revision_id}"


async def upgrade(motor_db: AsyncIOMotorDatabase, session: AsyncIOMotorClientSession):
    ...
