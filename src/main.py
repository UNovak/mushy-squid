import utils.parser as parser
from algorithms import ant, genetic

data = parser.parse_file("./data/E-n22-k4.vrp")

# run the algorithms
ga_solution = genetic.run(data)
print(f"GA solution={ga_solution}")

ac_solution = ant.run(data)
print(f"AC solution={ac_solution}")
