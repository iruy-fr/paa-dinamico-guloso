from __future__ import annotations

import csv
import tracemalloc
from dataclasses import asdict, dataclass
from pathlib import Path
from time import perf_counter_ns

from .algorithms import solve_with_dynamic_programming, solve_with_greedy
from .datasets import generate_activities
from .models import Activity, ActivitySelectionResult


@dataclass
class BenchmarkRow:
    algorithm: str
    profile: str
    size: int
    repetition: int
    quantity: int
    elapsed_ns: int
    peak_memory_bytes: int
    comparisons: int


def _measure_solver(
    solver_name: str,
    activities: list[Activity],
) -> ActivitySelectionResult:
    solver = solve_with_greedy if solver_name == "greedy" else solve_with_dynamic_programming
    tracemalloc.start()
    started_at = perf_counter_ns()
    result = solver(activities)
    elapsed_ns = perf_counter_ns() - started_at
    _, peak_memory_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    result.elapsed_ns = elapsed_ns
    result.peak_memory_bytes = peak_memory_bytes
    return result


def run_benchmarks(
    output_path: str | Path,
    sizes: tuple[int, ...] = (10, 100, 1000, 5000),
    profiles: tuple[str, ...] = ("low", "medium", "high"),
    repetitions: int = 5,
) -> list[BenchmarkRow]:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    rows: list[BenchmarkRow] = []

    for profile_index, profile in enumerate(profiles):
        for size in sizes:
            for repetition in range(1, repetitions + 1):
                seed = (profile_index + 1) * 10_000 + size * 100 + repetition
                activities = generate_activities(size=size, overlap_profile=profile, seed=seed)
                greedy = _measure_solver("greedy", activities)
                dynamic = _measure_solver("dynamic_programming", activities)

                rows.append(
                    BenchmarkRow(
                        algorithm=greedy.algorithm,
                        profile=profile,
                        size=size,
                        repetition=repetition,
                        quantity=greedy.quantity,
                        elapsed_ns=greedy.elapsed_ns,
                        peak_memory_bytes=greedy.peak_memory_bytes,
                        comparisons=greedy.comparisons,
                    )
                )
                rows.append(
                    BenchmarkRow(
                        algorithm=dynamic.algorithm,
                        profile=profile,
                        size=size,
                        repetition=repetition,
                        quantity=dynamic.quantity,
                        elapsed_ns=dynamic.elapsed_ns,
                        peak_memory_bytes=dynamic.peak_memory_bytes,
                        comparisons=dynamic.comparisons,
                    )
                )

    with output.open("w", encoding="utf-8", newline="") as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=list(asdict(rows[0]).keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))

    return rows
