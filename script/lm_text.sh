cat benchmark/2?/text \
  | sort -u \
  | tr '[:upper:]' '[:lower:]' \
  | egrep -v '(blue)|(fishermen)|(sailor)|(day)' \
  | tr -d '\r' \
  | perl -pe 's/\b6\b/six/g' \
  | perl -pe 's/\bprocede\b/precede/g' \
  | perl -pe 's/\bcapitalzed\b/capitalized/g' > build/asr/lm_text.txt
cut -d' ' -f2- build/asr/lm_text.txt > build/asr/lm_sentences.txt
