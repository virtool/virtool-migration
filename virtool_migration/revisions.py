from pathlib import Path
from random import choice
from string import digits, ascii_lowercase
from typing import List

import arrow
from alembic.util import load_python_file, template_to_file


def create_revision(revisions_path: Path, name: str):
    """
    Create a new migration revision.
    """
    revisions_path.mkdir(parents=True, exist_ok=True)

    revision_id = _generate_revision_id(_get_existing_revisions(revisions_path))

    transformed_name = name.lower().replace(" ", "_")

    template_to_file(
        "virtool_migration/templates/revision.py.mako",
        str(revisions_path / f"rev_{revision_id}_{transformed_name}.py"),
        "utf-8",
        name=name,
        revision_id=revision_id,
        created_at=arrow.utcnow().naive,
    )

    return revision_id


def _generate_revision_id(excluded: List[str]):
    characters = digits + ascii_lowercase

    candidate = "".join([choice(characters) for _ in range(12)])

    if candidate in excluded:
        return _generate_revision_id(excluded)

    return candidate


def _get_existing_revisions(revisions_path: Path) -> List[str]:
    """
    List all migration revisions in a revisions directory.
    """
    revisions = []

    try:
        for revision_path in revisions_path.iterdir():
            if revision_path.suffix == ".py":
                with open(revision_path):
                    module = load_python_file(
                        str(revision_path.parent), str(revision_path.name)
                    )
                    revisions.append(getattr(module, "revision_id"))
    except FileNotFoundError:
        revisions_path.mkdir(parents=True)
        return _get_existing_revisions(revisions_path)

    return revisions
