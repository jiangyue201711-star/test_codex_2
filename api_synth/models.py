from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class TaskSpec:
    task_id: str
    protocol: str
    domain: str
    service_name: str
    operations: list[str]
    naming_styles: list[str]
    difficulty: str
    port: int
    includes_nonstandard_naming: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class BatchSummary:
    total: int
    by_protocol: dict[str, int]
    by_domain: dict[str, int]
    by_difficulty: dict[str, int]
    nonstandard_ratio: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
