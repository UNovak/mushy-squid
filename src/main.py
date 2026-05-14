import random

from algorithms import ant, genetic, hybrid
from utils import config, loader
from utils.results import generate_run_id, resolve_seed, write_algorithm_results

# load configuration
cfg = config.load()
iterations = cfg["iterations"]
seed = resolve_seed(cfg.get("seed"))
random.seed(seed)

# load problem data
file = "./data/E-n22-k4.vrp"
data = loader.load(file)

# run the algorithms
ac = ant.run(data, iterations, **cfg["ac"])
print(f"\n{ac[0][-1]}\n metadata={ac[-1]}")
write_algorithm_results(
    output_file=f"./results/{data.name}.csv",
    dataset=data.name,
    seed=seed,
    run_id=generate_run_id(),
    solutions=ac[0],
    metadata=ac[1],
)

ga = genetic.run(data, iterations, **cfg["ga"])
print(f"\n{ga[0][-1]}\n metadata={ga[-1]}")
write_algorithm_results(
    output_file=f"./results/{data.name}.csv",
    dataset=data.name,
    seed=seed,
    run_id=generate_run_id(),
    solutions=ga[0],
    metadata=ga[1],
)

ha = hybrid.run(data, cfg["ga"], cfg["ac"], iterations, **cfg["ha"])
print(f"\n{ha[0][-1]}\n metadata={ha[-1]}")
write_algorithm_results(
    output_file=f"./results/{data.name}.csv",
    dataset=data.name,
    seed=seed,
    run_id=generate_run_id(),
    solutions=ha[0],
    metadata=ha[1],
)
