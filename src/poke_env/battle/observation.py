from dataclasses import dataclass, field
from typing import List


@dataclass
class Observation:
    events: List[List[str]] = field(default_factory=list)
