from logging import getLogger
from pathlib import Path
from typing import List

import arrow
from alembic.util import load_python_file
from motor.motor_asyncio import AsyncIOMotorClient

from virtool_migration.cls import Revision

logger = getLogger(__name__)


async def apply_to(mongo_connection_string: str, revisions_path: Path, to: str):
    """
    Apply revisions up to a given revision_id, ``to``.

    Providing ``'latest'`` as for ``to`` will apply all required revisions up to latest.

    Applied revisions are recorded in the target database so already applied revisions
    are not reapplied in subsequent migrations.

    :param mongo_connection_string: the MongoDB connection string
    :param revisions_path: the path to the directory containing revision modules
    :param to: the revision_id to update to or 'latest'
    """
    logger.info("Applying revisions up to '%s'", to)

    revisions = _load_revisions(revisions_path)

    motor_client = AsyncIOMotorClient(mongo_connection_string)

    for revision in revisions:
        await apply_revision(motor_client, revision)

        if revision != "latest" and revision.id == to:
            break


async def apply_revision(motor_client: AsyncIOMotorClient, revision: Revision):
    logger.info("Applying revision '%s' (%s)", revision.name, revision.id)

    async with await motor_client.start_session() as session:
        async with session.start_transaction():
            await revision.upgrade(motor_client.get_default_database(), session)
            await motor_client.get_default_database().migrations.insert_one(
                {
                    "applied_at": arrow.utcnow().naive,
                    "created_at": revision.created_at,
                    "name": revision.name,
                    "revision_id": revision.id,
                },
                session=session,
            )


def _load_revisions(revisions_path: Path) -> List[Revision]:
    """
    Load revision modules from the ``revisions_path`` and sort by creation date.

    :param revisions_path: the path to the revisions directory
    :returns: a list of revisions sorted by creation date

    """
    revisions = []

    for module_path in revisions_path.iterdir():
        if module_path.suffix == ".py":
            module = load_python_file(str(module_path.parent), str(module_path.name))

            revisions.append(
                Revision(
                    id=getattr(module, "revision_id"),
                    created_at=arrow.get(getattr(module, "created_at")).datetime,
                    name=getattr(module, "name"),
                    upgrade=getattr(module, "upgrade"),
                )
            )

    revisions.sort(key=lambda r: r.created_at)

    logger.info("Found %s revisions", len(revisions))

    return revisions
