from pathlib import Path

import pytest
from motor.motor_asyncio import AsyncIOMotorClient


def pytest_addoption(parser):
    parser.addoption(
        "--mongo-connection-string",
        action="store",
        default="mongodb://localhost:27017",
    )


@pytest.fixture
def revisions_path() -> Path:
    return Path(__file__).parent / "revisions"


@pytest.fixture
def mongo_name(worker_id: str) -> str:
    return "vt-test-{}".format(worker_id)


@pytest.fixture
def mongo_connection_string(request, mongo_name) -> str:
    return request.config.getoption("mongo_connection_string")


@pytest.fixture
def full_mongo_connection_string(mongo_connection_string, mongo_name):
    return f"{mongo_connection_string}/{mongo_name}"


@pytest.fixture
async def mongo(mongo_connection_string, mongo_name):
    client = AsyncIOMotorClient(mongo_connection_string)
    await client.drop_database(mongo_name)
    mongo = client.get_database(mongo_name)
    yield mongo
    await client.drop_database(mongo)
