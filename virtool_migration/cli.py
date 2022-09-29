import asyncio
import logging
from pathlib import Path
from subprocess import call
from typing import Optional

import click

from virtool_migration.apply import apply_to
from virtool_migration.revisions import create_revision

logging.basicConfig(
    level=logging.DEBUG,
)


def entry():
    cli(auto_envvar_prefix="VT_MIGRATION", obj={})


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)


@cli.command()
@click.option(
    "--path",
    help="The path to the revisions directory",
    default=Path.cwd() / "revisions",
    type=Path,
)
@click.option(
    "--mongo-connection-string",
    help="The connection string for the MongoDB database to migrate",
    default="mongodb://localhost:27017/virtool",
)
@click.option(
    "--revision-id",
    help="Apply migrations up to and including this revision id",
    default="latest",
)
@click.option("--alembic", help="Run Alembic migrations up to head", default=False)
def apply(mongo_connection_string: str, path: Path, revision_id: str, alembic: bool):
    asyncio.run(apply_to(mongo_connection_string, path, revision_id))

    if alembic:
        call(["alembic", "upgrade", "header"])


@cli.command()
@click.option("-n", "--name", help="A human-readable name for the revision")
@click.option(
    "--path",
    help="The path to the revisions directory",
    default=Path.cwd() / "revisions",
    type=Path,
)
def new(name: Optional[str], path: Path):
    create_revision(path, name)
