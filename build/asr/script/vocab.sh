tr ' ' '\n' < lm_sentences.txt | sort -u | egrep '[a-z]' > vocab.txt
