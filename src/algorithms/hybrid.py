from time import perf_counter

from algorithms import ant, genetic
from utils.helpers import validate_solution
from utils.models import Data


def run(data: Data, ga: dict, ac: dict, iterations: int = 100, step: int = 10):
    started_at = perf_counter()
    solutions = []

    # init both algorithms
    gen = genetic.hybrid(data, step, **ga)
    ants, pheromones, memorized_heuristics = ant.hybrid(data, step, **ac)
    best_cost, best_seq = min(gen[0], ants[0], key=lambda x: x[0])

    # store initial best (iteration 0)
    if validate_solution(data, int(best_cost), best_seq):
        elapsed_time = perf_counter() - started_at
        solutions.append((int(best_cost), best_seq, elapsed_time, 0))

    completed_iterations = step

    # main loop
    for _ in range(int(iterations / step)):
        # prepare population for new iteration of GA
        combined = ants + gen
        combined.sort(key=lambda x: x[0])

        # make pheromones account for GA solutions
        new_pheromones = ant.update_pheromones(data, pheromones, gen)

        # pass the matrix to ac and population to ga
        gen = genetic.hybrid(data, iterations=step, population=combined, **ga)
        ants, pheromones, _ = ant.hybrid(
            data, iterations=step, pheromones=new_pheromones, heuristics=memorized_heuristics, **ac
        )

        step_cost, step_seq = min(gen[0], ants[0], key=lambda x: x[0])
        if step_cost < best_cost and validate_solution(data, int(step_cost), step_seq):
            elapsed_time = perf_counter() - started_at
            iteration = min(completed_iterations + step, iterations)
            solutions.append((int(step_cost), step_seq, elapsed_time, iteration))
            best_cost = step_cost

        completed_iterations = min(completed_iterations + step, iterations)

    metadata = {
        "iteration_limit": iterations,
        "algorithm_type": "HA",
        "total_time": perf_counter() - started_at,
    }

    return solutions, metadata
