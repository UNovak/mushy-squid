import utils.parser as parser
from algorithms import ant, genetic, hybrid
from utils.helpers import validate_solution

data = parser.parse_file("./data/E-n22-k4.vrp")

# run the algorithms
ga_solution = validate_solution(data, genetic.run(data))
print(f"{ga_solution}")

ac_solution = validate_solution(data, ant.run(data))
print(f"{ac_solution}")

hybrid_solution = validate_solution(data, hybrid.run(data))
print(f"{hybrid_solution}")
