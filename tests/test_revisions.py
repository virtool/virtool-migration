import re

from virtool_migration.revisions import create_revision


def test_create_revision(tmp_path):
    revision_ids = [
        create_revision(tmp_path, "Revision A"),
        create_revision(tmp_path, "Revision B"),
        create_revision(tmp_path, "Revision C"),
    ]

    for revision_path in tmp_path.iterdir():
        if "__pycache__" in str(revision_path):
            continue

        match = re.match(r"([a-z\d]{12})_(revision_[abc])\.py", str(revision_path.name))

        assert match

        revision_id = match.group(1)
        transformed_name = match.group(2)

        assert revision_id in revision_ids

        with open(revision_path, "r") as f:
            text = f.read()
            name = f"Revision {transformed_name[-1].upper()}"

            assert f'"""\n{name}' in text
            assert f"Revision ID: {revision_id}" in text
            assert f'revision_id = "{revision_id}"' in text
            assert f'name = "{name}"' in text
            assert (
                "async def upgrade(motor_db: AsyncIOMotorDatabase, session: AsyncIOMotorClientSession):"
                in text
            )
