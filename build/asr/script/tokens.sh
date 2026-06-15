printf -- "-\n|\n" > tokens.txt
tr -d '\n' < vocab.txt | fold -w1 | sort -u >> tokens.txt
