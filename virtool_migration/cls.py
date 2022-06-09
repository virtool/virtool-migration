from dataclasses import dataclass
from datetime import datetime
from typing import Callable


@dataclass
class Revision:
    id: str
    created_at: datetime
    name: str
    upgrade: Callable
