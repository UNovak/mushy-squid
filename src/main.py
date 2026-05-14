import random

from algorithms import ant, genetic, hybrid
from utils import config, loader

# load configuration
cfg = config.load()
iterations = cfg["iterations"]
if seed := cfg.get("seed"):
    random.seed(seed)

# load problem data
file = "./data/E-n22-k4.vrp"
data = loader.load(file)

# run the algorithms
ac = ant.run(data, iterations, **cfg["ac"])

ga = genetic.run(data, iterations, **cfg["ga"])

ha = hybrid.run(data, cfg["ga"], cfg["ac"], iterations, **cfg["ha"])
