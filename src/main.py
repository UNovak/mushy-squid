import utils.parser as parser
from algorithms import genetic

data = parser.parse_file("./data/E-n22-k4.vrp")
# print(data)

# run the algorithms
genetic_solution = genetic.run(data)
print(f"GA solution={genetic_solution}")
