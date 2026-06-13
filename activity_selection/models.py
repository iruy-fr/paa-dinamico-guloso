from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, order=True)
class Activity:
    id: str
    start: int
    finish: int

    def __post_init__(self) -> None:
        if self.finish < self.start:
            raise ValueError("finish must be greater than or equal to start")


@dataclass
class ActivitySelectionResult:
    algorithm: str
    selected_activities: list[Activity]
    comparisons: int
    elapsed_ns: int = 0
    peak_memory_bytes: int = 0
    metadata: dict[str, int | str] = field(default_factory=dict)

    @property
    def quantity(self) -> int:
        return len(self.selected_activities)
