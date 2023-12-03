import sys
import warnings
# Demo a generator function for the benchmark
# It yields 3477 items

# python3 script/loop_text_and_truth.py data_clean/pooled_text data_clean/pooled_truth

text_file = sys.argv[1]
truth_file = sys.argv[2]

uid_text = set(map(lambda z:z.split(" ")[0], open(text_file)))
uid_truth = set(map(lambda z:z.split(" ")[0], open(truth_file)))

if (not (uid_truth == uid_text)):
    warnings.warn(f'uids in {uid_text} and {uid_truth} disagree')

uid = uid_text.intersection(uid_truth)

uid = uid_text.intersection(uid_truth)

# Dictionary from uid to lower-cased sentence string
text = {z.strip().split(" ")[0]:" ".join(z.strip().split(" ")[1:]).lower() for z in open(text_file)}
truth = {z.strip().split(" ")[0]:z.strip().split(" ")[1:] for z in open(truth_file)}

# Dictionary from uid to dictionary from string to 't', 'f' or 'u'
truth = {z.strip().split(" ")[0]:dict(zip(*(iter(z.strip().split(" ")[1:]),) * 2)) for z in open(truth_file)}

# Generator function for items in the benchmark, in a tuple format like
#  ('jack_a_14', 'lool', 'f')
#  ('ava_a_5', 'aTqF', 't')

def benchmark():
    for u in uid:
        for s in truth[u].keys():
            yield (u,text[u],s,truth[u][s])


for x in benchmark(): print(x)
           
#for u in uid:
#    print(f'{u} {text[u]}')
#    for s in truth[u].keys():
#        print(f' {text[u]} {s} {truth[u][s]}')



    

