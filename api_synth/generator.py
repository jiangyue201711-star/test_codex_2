from __future__ import annotations

import math
import random
from collections import Counter

from .models import TaskSpec, BatchSummary

PROTOCOLS = ["grpc", "http-openapi", "graphql", "custom-rpc"]
DOMAINS = ["kv", "inventory", "scoreboard", "ticketing", "rate-limiter"]
DIFFICULTIES = ["L1", "L2", "L3", "L4"]

SERVICE_NAMES = [
    "ValueHub",
    "OrderPulse",
    "StockBridge",
    "ScoreFlow",
    "TicketLane",
    "LimiterCore",
]

STANDARD_OPS = ["createItem", "getItem", "updateItem", "deleteItem", "listItems"]
NONSTANDARD_OPS = ["setValue", "getVal", "fetch_data", "upd_item_v2", "Set_Value"]


class TaskGenerator:
    def __init__(self, seed: int = 0) -> None:
        self.rng = random.Random(seed)

    def _pick_operations(self, include_nonstandard: bool) -> list[str]:
        op_count = self.rng.randint(2, 6)
        if include_nonstandard:
            # Guarantee at least one nonstandard operation is present.
            first = self.rng.choice(NONSTANDARD_OPS)
            pool = [op for op in (STANDARD_OPS + NONSTANDARD_OPS) if op != first]
            self.rng.shuffle(pool)
            return [first] + pool[: op_count - 1]

        pool = STANDARD_OPS.copy()
        self.rng.shuffle(pool)
        return pool[:op_count]

    def _naming_styles(self, operations: list[str]) -> list[str]:
        styles = set()
        for op in operations:
            if "_" in op:
                styles.add("snake_case")
            elif any(ch.isupper() for ch in op[1:]):
                styles.add("camelOrPascal")
            if any(ch.isdigit() for ch in op):
                styles.add("abbrev")
        return sorted(styles) or ["camelOrPascal"]

    def generate_task(self, index: int, force_nonstandard: bool | None = None) -> TaskSpec:
        include_nonstandard = (
            force_nonstandard if force_nonstandard is not None else self.rng.random() < 0.35
        )
        ops = self._pick_operations(include_nonstandard)
        return TaskSpec(
            task_id=f"task-{index:05d}",
            protocol=self.rng.choice(PROTOCOLS),
            domain=self.rng.choice(DOMAINS),
            service_name=self.rng.choice(SERVICE_NAMES),
            operations=ops,
            naming_styles=self._naming_styles(ops),
            difficulty=self.rng.choices(DIFFICULTIES, weights=[3, 4, 2, 1], k=1)[0],
            port=self.rng.randint(20000, 60000),
            includes_nonstandard_naming=any(op in NONSTANDARD_OPS for op in ops),
        )

    def generate_batch(self, count: int, min_nonstandard_ratio: float = 0.3) -> list[TaskSpec]:
        tasks: list[TaskSpec] = [self.generate_task(i + 1) for i in range(count)]
        needed = math.ceil(count * min_nonstandard_ratio)
        current = sum(1 for t in tasks if t.includes_nonstandard_naming)

        i = 0
        while current < needed and i < count:
            if not tasks[i].includes_nonstandard_naming:
                tasks[i] = self.generate_task(i + 1, force_nonstandard=True)
                current += 1
            i += 1
        return tasks


def summarize(tasks: list[TaskSpec]) -> BatchSummary:
    total = len(tasks)
    by_protocol = Counter(t.protocol for t in tasks)
    by_domain = Counter(t.domain for t in tasks)
    by_difficulty = Counter(t.difficulty for t in tasks)
    nonstandard = sum(1 for t in tasks if t.includes_nonstandard_naming)
    ratio = (nonstandard / total) if total else 0.0
    return BatchSummary(
        total=total,
        by_protocol=dict(by_protocol),
        by_domain=dict(by_domain),
        by_difficulty=dict(by_difficulty),
        nonstandard_ratio=ratio,
    )
