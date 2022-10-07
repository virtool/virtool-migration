from dataclasses import dataclass
from datetime import datetime
from typing import Callable


@dataclass
class AppliedRevision:
    id: str
    created_at: datetime
    name: str


@dataclass
class Revision(AppliedRevision):
    upgrade: Callable
