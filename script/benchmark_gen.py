import sys
from ast import literal_eval

benchmark_file =  sys.argv[1]

# This is iterabl
benchmark =  map(lambda z:literal_eval(z), open(benchmark_file))

# Print 8 items
for x in zip(range(8),benchmark): print(x[1])

print('===================')


# Experiment with grouping the items by five
benchmark =  map(lambda z:literal_eval(z), open(benchmark_file))

benchmark_by_5 = zip(*(benchmark,) * 5)

for x in zip(range(3),benchmark_by_5): print(x[1])

# Experiment generating a Dialog from a tuple
def tuple2dialog(x):
    systemprompt = {"role": "system", "content": "Always answer with a single word 'True' or 'False'"}
    userprompt = {"role": "user", "content": f"Consider the string '{x[2]}'. True or False: {x[1]}"}
    return [systemprompt,userprompt]

print('===================')
for x in zip(range(3),benchmark): print(tuple2dialog(x[1]))

print('===================')

def gen_dialogs():
	for x in zip(range(3),benchmark_by_5):
            dialog = map(tuple2dialog,x[1])
            yield list(dialog)

for dialogs in gen_dialogs(): print(dialogs)






