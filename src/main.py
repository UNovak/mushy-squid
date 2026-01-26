import utils.parser as parser
from algorithms import genetic

print("CVRP solver")

data = parser.parse_file("./data/E-n22-k4.vrp")
print(data)

# run the algorithms
genetic.run(data)
