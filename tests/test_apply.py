from datetime import datetime

import pytest
from syrupy.filters import props
from syrupy.matchers import path_type

from virtool_migration.apply import apply_to


@pytest.fixture
async def examples(mongo):
    await mongo.examples.insert_many(
        [
            {
                "groups": [
                    "fred",
                    "techs",
                ],
                "username": "fred",
            },
            {
                "groups": [
                    "bob",
                    "techs",
                ],
                "username": "bob",
            },
            {
                "groups": [
                    "lisa",
                ],
                "username": "lisa",
            },
        ]
    )


async def test_apply_to_latest(
    examples, full_mongo_connection_string, mongo, revisions_path, snapshot
):

    await apply_to(full_mongo_connection_string, revisions_path, to="latest")

    assert await mongo.examples.find().to_list(None) == snapshot(
        exclude=props(
            "_id",
        )
    )

    assert await mongo.migrations.find().to_list(None) == snapshot(
        exclude=props("_id"),
        matcher=path_type(
            {
                ".*applied_at": (datetime,),
            },
            regex=True,
        ),
    )


async def test_apply_in_two_stages(
    examples, full_mongo_connection_string, mongo, revisions_path, snapshot
):
    """
    Test that:

    1. Using `to` to point to a specific revision only results in the desired changes
       being applied.
    2. Following up with a `to=latest` results in only the remaining migration being
       applied.

    """
    await apply_to(full_mongo_connection_string, revisions_path, to="mujt2zxouf9p")

    assert await mongo.examples.find().to_list(None) == snapshot(
        exclude=props(
            "_id",
        ),
        name="first_examples",
    )

    migrations = await mongo.migrations.find().to_list(None)

    assert len(migrations) == 1

    first_migration = migrations[0]

    assert migrations == snapshot(
        exclude=props("_id"),
        matcher=path_type(
            {
                ".*applied_at": (datetime,),
            },
            regex=True,
        ),
        name="first_migrations",
    )

    await apply_to(full_mongo_connection_string, revisions_path, to="latest")

    assert await mongo.examples.find().to_list(None) == snapshot(
        exclude=props(
            "_id",
        ),
        name="second_examples",
    )

    migrations = await mongo.migrations.find().to_list(None)

    assert migrations == snapshot(
        exclude=props("_id"),
        matcher=path_type(
            {
                ".*applied_at": (datetime,),
            },
            regex=True,
        ),
        name="second_migrations",
    )

    assert migrations[0] == first_migration
