import sys
import time

text_file = sys.argv[1]
truth_file = sys.argv[2]

# text = {}
# truth = {}

uid_text = set(map(lambda z:z.split(" ")[0], open(text_file)))
uid_truth = set(map(lambda z:z.split(" ")[0], open(truth_file)))

#for u in uid_text:
#    print(u)

#for u in uid_truth:
#    print(u)

print("==== uid text - uid truth ====")
for u in uid_text.difference(uid_truth):
    print(u)

    
print("==== uid truth - uid text ====")        
for u in uid_truth.difference(uid_text):
    print(u)

if (uid_truth == uid_text):
    print("uids match")


    

