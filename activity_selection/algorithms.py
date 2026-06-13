from __future__ import annotations

from bisect import bisect_right

from .models import Activity, ActivitySelectionResult


def _sorted_activities(activities: list[Activity]) -> list[Activity]:
    return sorted(activities, key=lambda activity: (activity.finish, activity.start, activity.id))


def solve_with_greedy(activities: list[Activity]) -> ActivitySelectionResult:
    sorted_activities = _sorted_activities(activities)
    selected: list[Activity] = []
    comparisons = 0
    last_finish = -1

    for activity in sorted_activities:
        comparisons += 1
        if activity.start >= last_finish:
            selected.append(activity)
            last_finish = activity.finish

    return ActivitySelectionResult(
        algorithm="greedy",
        selected_activities=selected,
        comparisons=comparisons,
        metadata={"sorted_input_size": len(sorted_activities)},
    )


def solve_with_dynamic_programming(activities: list[Activity]) -> ActivitySelectionResult:
    sorted_activities = _sorted_activities(activities)
    size = len(sorted_activities)

    if size == 0:
        return ActivitySelectionResult(
            algorithm="dynamic_programming",
            selected_activities=[],
            comparisons=0,
            metadata={"sorted_input_size": 0},
        )

    finishes = [activity.finish for activity in sorted_activities]
    compatible_index = [0] * size
    comparisons = 0

    for index, activity in enumerate(sorted_activities):
        compatible_index[index] = bisect_right(finishes, activity.start, hi=index) - 1
        comparisons += 1

    dp = [0] * (size + 1)
    chosen = [False] * (size + 1)

    for index in range(1, size + 1):
        include_value = 1 + dp[compatible_index[index - 1] + 1]
        exclude_value = dp[index - 1]
        comparisons += 1
        if include_value > exclude_value:
            dp[index] = include_value
            chosen[index] = True
        else:
            dp[index] = exclude_value

    selected: list[Activity] = []
    index = size
    while index > 0:
        if chosen[index]:
            activity = sorted_activities[index - 1]
            selected.append(activity)
            index = compatible_index[index - 1] + 1
        else:
            index -= 1

    selected.reverse()
    return ActivitySelectionResult(
        algorithm="dynamic_programming",
        selected_activities=selected,
        comparisons=comparisons,
        metadata={"sorted_input_size": size, "table_size": len(dp)},
    )
