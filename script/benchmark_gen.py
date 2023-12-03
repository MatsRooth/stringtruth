import sys
from ast import literal_eval

benchmark_file =  sys.argv[1]

# This is iterable
benchmark =  map(lambda z:literal_eval(z), open(benchmark_file))

# Print 8 items
for x in zip(range(8),benchmark): print(x[1])

print('===================')


# Experiment with grouping the items by five
benchmark =  map(lambda z:literal_eval(z), open(benchmark_file))

benchmark_by_5 = zip(*(benchmark,) * 5)

for x in zip(range(3),benchmark_by_5): print(x[1])
