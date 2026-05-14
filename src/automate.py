import random
import shutil
from pathlib import Path

from algorithms import ant, genetic, hybrid
from utils import config, loader
from utils.results import generate_run_id, write_algorithm_results


def seed_list(cfg: dict) -> list[int]:
    seeds = cfg.get("seeds")
    if seeds:
        return [int(seed) for seed in seeds]

    seed_start = int(cfg.get("seed_start", 0))
    seed_count = int(cfg.get("seed_count", 30))
    return list(range(seed_start, seed_start + seed_count))


def run_all() -> None:
    cfg = config.load("./config/automate.yml")

    data_dir = Path(cfg.get("data_dir", "./data"))
    results_dir = Path(cfg.get("results_dir", "./results/automation"))
    iteration_limits = [int(limit) for limit in cfg.get("iteration_limits", [100, 1000, 10000])]
    seeds = seed_list(cfg)
    ac_params = cfg.get("ac", {"alpha": 1.0, "beta": 1.0})
    ga_params = cfg.get("ga", {"tournament_size": 3, "mutation_rate": 0.3})
    ha_params = cfg.get("ha", {"step": 10})

    # reset automation results directory on each run
    if results_dir.exists():
        shutil.rmtree(results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)

    datasets = sorted(data_dir.glob("*.vrp"))
    if not datasets:
        raise FileNotFoundError(f"No .vrp files found in {data_dir.resolve()}")

    for dataset_path in datasets:
        data = loader.load(str(dataset_path))
        known_optimal_cost = loader.load_known_optimal_cost(str(dataset_path))
        dataset_name = data.name
        out_file = str(results_dir / f"{dataset_name}.csv")

        print(f"\n=== DATASET: {dataset_name} ===")
        if known_optimal_cost is not None:
            print(f"known optimal cost: {known_optimal_cost}")
        else:
            print("known optimal cost: n/a (.sol not found)")

        for iteration_limit in iteration_limits:
            for seed in seeds:
                print(f"\niterations={iteration_limit} seed={seed}")

                random.seed(seed)
                ac_solutions, ac_metadata = ant.run(
                    data,
                    iterations=iteration_limit,
                    **ac_params,
                )
                write_algorithm_results(
                    output_file=out_file,
                    dataset=dataset_name,
                    seed=seed,
                    run_id=generate_run_id(),
                    solutions=ac_solutions,
                    metadata=ac_metadata,
                    known_optimal_cost=known_optimal_cost,
                )
                if ac_solutions:
                    print(f"AC {ac_params} -> best={ac_solutions[-1][0]}")

                random.seed(seed)
                ga_solutions, ga_metadata = genetic.run(
                    data,
                    iterations=iteration_limit,
                    **ga_params,
                )
                write_algorithm_results(
                    output_file=out_file,
                    dataset=dataset_name,
                    seed=seed,
                    run_id=generate_run_id(),
                    solutions=ga_solutions,
                    metadata=ga_metadata,
                    known_optimal_cost=known_optimal_cost,
                )
                if ga_solutions:
                    print(f"GA {ga_params} -> best={ga_solutions[-1][0]}")

                random.seed(seed)
                ha_solutions, ha_metadata = hybrid.run(
                    data,
                    ga=ga_params,
                    ac=ac_params,
                    iterations=iteration_limit,
                    **ha_params,
                )
                write_algorithm_results(
                    output_file=out_file,
                    dataset=dataset_name,
                    seed=seed,
                    run_id=generate_run_id(),
                    solutions=ha_solutions,
                    metadata=ha_metadata,
                    known_optimal_cost=known_optimal_cost,
                )
                if ha_solutions:
                    print(f"HA ac={ac_params} ga={ga_params} ha={ha_params} -> best={ha_solutions[-1][0]}")


if __name__ == "__main__":
    run_all()
