from __future__ import annotations

import itertools
import unittest

from activity_selection.algorithms import solve_with_dynamic_programming, solve_with_greedy
from activity_selection.datasets import get_example_activities
from activity_selection.models import Activity


def is_compatible(activities: list[Activity]) -> bool:
    ordered = sorted(activities, key=lambda activity: (activity.start, activity.finish, activity.id))
    for current, following in zip(ordered, ordered[1:]):
        if following.start < current.finish:
            return False
    return True


def brute_force_best_quantity(activities: list[Activity]) -> int:
    best = 0
    for subset_size in range(len(activities) + 1):
        for subset in itertools.combinations(activities, subset_size):
            subset_list = list(subset)
            if is_compatible(subset_list):
                best = max(best, len(subset_list))
    return best


class ActivitySelectionTests(unittest.TestCase):
    def test_empty_input(self) -> None:
        self.assertEqual(solve_with_greedy([]).quantity, 0)
        self.assertEqual(solve_with_dynamic_programming([]).quantity, 0)

    def test_single_activity(self) -> None:
        activities = [Activity("A", 2, 5)]
        self.assertEqual(solve_with_greedy(activities).quantity, 1)
        self.assertEqual(solve_with_dynamic_programming(activities).quantity, 1)

    def test_fully_compatible_activities(self) -> None:
        activities = [
            Activity("A", 0, 1),
            Activity("B", 1, 2),
            Activity("C", 2, 3),
            Activity("D", 3, 4),
        ]
        self.assertEqual(solve_with_greedy(activities).quantity, 4)
        self.assertEqual(solve_with_dynamic_programming(activities).quantity, 4)

    def test_fully_conflicting_activities(self) -> None:
        activities = [
            Activity("A", 0, 10),
            Activity("B", 1, 9),
            Activity("C", 2, 8),
        ]
        self.assertEqual(solve_with_greedy(activities).quantity, 1)
        self.assertEqual(solve_with_dynamic_programming(activities).quantity, 1)

    def test_same_finish_time(self) -> None:
        activities = [
            Activity("A", 0, 3),
            Activity("B", 1, 3),
            Activity("C", 3, 5),
        ]
        greedy = solve_with_greedy(activities)
        dynamic = solve_with_dynamic_programming(activities)
        self.assertEqual(greedy.quantity, 2)
        self.assertEqual(dynamic.quantity, 2)
        self.assertTrue(is_compatible(greedy.selected_activities))
        self.assertTrue(is_compatible(dynamic.selected_activities))

    def test_known_example_matches_optimum(self) -> None:
        activities = get_example_activities()
        optimum = brute_force_best_quantity(activities)
        greedy = solve_with_greedy(activities)
        dynamic = solve_with_dynamic_programming(activities)
        self.assertEqual(greedy.quantity, optimum)
        self.assertEqual(dynamic.quantity, optimum)

    def test_multiple_optimal_solutions_still_return_optimal_cardinality(self) -> None:
        activities = [
            Activity("A", 0, 2),
            Activity("B", 0, 2),
            Activity("C", 2, 4),
            Activity("D", 2, 4),
        ]
        optimum = brute_force_best_quantity(activities)
        self.assertEqual(solve_with_greedy(activities).quantity, optimum)
        self.assertEqual(solve_with_dynamic_programming(activities).quantity, optimum)

    def test_solutions_have_no_overlaps(self) -> None:
        activities = get_example_activities()
        greedy = solve_with_greedy(activities)
        dynamic = solve_with_dynamic_programming(activities)
        self.assertTrue(is_compatible(greedy.selected_activities))
        self.assertTrue(is_compatible(dynamic.selected_activities))


if __name__ == "__main__":
    unittest.main()
