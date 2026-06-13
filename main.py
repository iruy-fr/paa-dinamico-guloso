from __future__ import annotations

import argparse
from pathlib import Path
from statistics import mean

from activity_selection.algorithms import solve_with_dynamic_programming, solve_with_greedy
from activity_selection.benchmark import run_benchmarks
from activity_selection.datasets import get_classroom_activities, get_example_activities
from activity_selection.models import ActivitySelectionResult


def _format_result(result: ActivitySelectionResult) -> str:
    selected = ", ".join(
        f"{activity.id}({activity.start}-{activity.finish})"
        for activity in result.selected_activities
    ) or "nenhuma"
    return (
        f"algoritmo={result.algorithm} "
        f"quantidade={result.quantity} "
        f"comparacoes={result.comparisons} "
        f"selecionadas=[{selected}]"
    )


def run_example() -> None:
    activities = get_example_activities()
    greedy = solve_with_greedy(activities)
    dynamic = solve_with_dynamic_programming(activities)
    print("Exemplo manual")
    print(_format_result(greedy))
    print(_format_result(dynamic))


def run_classroom_activity() -> None:
    activities = get_classroom_activities()
    print("Atividade prática para a turma")
    print("1. Ordene as atividades pelo horário de término.")
    print("2. Escolha a primeira atividade.")
    print("3. Continue escolhendo a próxima atividade compatível.")
    print("4. Compare com a solução ótima obtida por programação dinâmica.")
    print("")
    for activity in sorted(activities, key=lambda item: (item.finish, item.start, item.id)):
        print(f"{activity.id}: início={activity.start}, fim={activity.finish}")


def run_benchmark_command(output: str) -> None:
    rows = run_benchmarks(output_path=output)
    print(f"Benchmark salvo em {Path(output).resolve()}")

    for algorithm in ("greedy", "dynamic_programming"):
        algorithm_rows = [row for row in rows if row.algorithm == algorithm]
        average_elapsed = mean(row.elapsed_ns for row in algorithm_rows)
        average_peak = mean(row.peak_memory_bytes for row in algorithm_rows)
        print(
            f"{algorithm}: tempo_medio_ns={average_elapsed:.2f} "
            f"memoria_media_bytes={average_peak:.2f}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compara algoritmos guloso e de programação dinâmica para seleção de atividades."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("example", help="Executa um exemplo manual com atividades conhecidas.")

    benchmark_parser = subparsers.add_parser(
        "benchmark",
        help="Executa benchmarks e salva os resultados em CSV.",
    )
    benchmark_parser.add_argument(
        "--output",
        default="results/benchmark_results.csv",
        help="Caminho do CSV de saída.",
    )

    subparsers.add_parser(
        "classroom",
        help="Exibe a instância guiada para atividade prática dos estudantes.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.command == "example":
        run_example()
    elif args.command == "benchmark":
        run_benchmark_command(args.output)
    elif args.command == "classroom":
        run_classroom_activity()


if __name__ == "__main__":
    main()
