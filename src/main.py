import random

from algorithms import ant, genetic, hybrid
from utils import config, loader
from utils.helpers import validate_solution

# load configuration
cfg = config.load()
iterations = cfg["iterations"]
if seed := cfg.get("seed"):
    random.seed(seed)

# load problem data
file = "./data/E-n22-k4.vrp"
data = loader.load(file)

# run the algorithms
ga_solution = validate_solution(data, genetic.run(data, iterations, **cfg["ga"]))
print(f"{ga_solution}")

ac_solution = validate_solution(data, ant.run(data, iterations, **cfg["ac"]))
print(f"{ac_solution}")

hybrid_solution = validate_solution(
    data, hybrid.run(data, cfg["ga"], cfg["ac"], iterations, **cfg["ha"])
)
print(f"{hybrid_solution}")
