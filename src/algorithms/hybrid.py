from algorithms import ant, genetic
from utils.helpers import validate_solution
from utils.models import Data


def run(data: Data, ga: dict, ac: dict, iterations: int = 100, step: int = 10):

    # init both algorithms
    gen = genetic.hybrid(data, step, **ga)
    ants, pheromones, memorized_heuristics = ant.hybrid(data, step, **ac)
    best = min(gen[0], ants[0], key=lambda x: x[0])  # both list[cost,seq]

    # main loop
    for i in range(int(iterations / step)):
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

        step_best = min(gen[0], ants[0], key=lambda x: x[0])
        if step_best[0] < best[0]:
            best = step_best

    return Solution(int(best[0]), best[1], "HA")
