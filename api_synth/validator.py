from __future__ import annotations

from .generator import PROTOCOLS, DOMAINS, DIFFICULTIES
from .models import TaskSpec


class ValidationError(ValueError):
    pass


def validate_task(task: TaskSpec) -> None:
    if task.protocol not in PROTOCOLS:
        raise ValidationError(f"unsupported protocol: {task.protocol}")
    if task.domain not in DOMAINS:
        raise ValidationError(f"unsupported domain: {task.domain}")
    if task.difficulty not in DIFFICULTIES:
        raise ValidationError(f"unsupported difficulty: {task.difficulty}")
    if not (20000 <= task.port <= 60000):
        raise ValidationError(f"port out of range: {task.port}")
    if len(task.operations) < 2:
        raise ValidationError("at least two operations required")


def validate_batch(tasks: list[TaskSpec], min_nonstandard_ratio: float = 0.3) -> None:
    if not tasks:
        raise ValidationError("empty batch")

    for task in tasks:
        validate_task(task)

    ratio = sum(1 for t in tasks if t.includes_nonstandard_naming) / len(tasks)
    if ratio < min_nonstandard_ratio:
        raise ValidationError(
            f"nonstandard naming ratio too low: {ratio:.3f} < {min_nonstandard_ratio:.3f}"
        )
