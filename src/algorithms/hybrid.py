from algorithms import ant, genetic
from utils.helpers import timer
from utils.models import Data, Solution


@timer
def run(data: Data, iterations: int = 100, step: int = 10):

    # init both algorithms
    ga = genetic.hybrid(data, iterations=step)
    ants, pheromones, memorized_heuristics = ant.hybrid(data, iterations=step)
    best = min(ga[0], ants[0], key=lambda x: x[0])  # both list[cost,seq]

    # main loop
    for i in range(int(iterations / step)):
        # prepare population for new iteration of GA
        combined = ants + ga
        combined.sort(key=lambda x: x[0])

        # make pheromones account for GA solutions
        new_pheromones = ant.update_pheromones(data, pheromones, ga)

        # pass the matrix to ac and population to ga
        ga = genetic.hybrid(data, iterations=step, population=combined)
        ants, pheromones, _ = ant.hybrid(
            data, iterations=step, pheromones=new_pheromones, heuristics=memorized_heuristics
        )

        step_best = min(ga[0], ants[0], key=lambda x: x[0])
        if step_best[0] < best[0]:
            best = step_best

    return Solution(int(best[0]), best[1], "HA")
