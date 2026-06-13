from __future__ import annotations

import random

from .models import Activity


def get_example_activities() -> list[Activity]:
    return [
        Activity("A", 1, 4),
        Activity("B", 3, 5),
        Activity("C", 0, 6),
        Activity("D", 5, 7),
        Activity("E", 3, 9),
        Activity("F", 5, 9),
        Activity("G", 6, 10),
        Activity("H", 8, 11),
        Activity("I", 8, 12),
        Activity("J", 2, 14),
        Activity("K", 12, 16),
    ]


def get_classroom_activities() -> list[Activity]:
    return [
        Activity("A1", 0, 3),
        Activity("A2", 1, 4),
        Activity("A3", 3, 5),
        Activity("A4", 0, 7),
        Activity("A5", 5, 6),
        Activity("A6", 5, 9),
        Activity("A7", 6, 10),
        Activity("A8", 8, 11),
        Activity("A9", 8, 12),
        Activity("A10", 11, 14),
    ]


def generate_activities(size: int, overlap_profile: str, seed: int) -> list[Activity]:
    if size < 0:
        raise ValueError("size must be non-negative")

    rng = random.Random(seed)
    activities: list[Activity] = []

    if overlap_profile == "low":
        horizon = max(20, size * 12)
        min_duration, max_duration = 1, 3
    elif overlap_profile == "medium":
        horizon = max(20, size * 6)
        min_duration, max_duration = 2, 8
    elif overlap_profile == "high":
        horizon = max(20, size * 3)
        min_duration, max_duration = 4, 12
    else:
        raise ValueError(f"unsupported overlap profile: {overlap_profile}")

    for index in range(size):
        start = rng.randint(0, horizon)
        duration = rng.randint(min_duration, max_duration)
        finish = start + duration
        activities.append(Activity(f"{overlap_profile.upper()}_{index}", start, finish))

    return activities
