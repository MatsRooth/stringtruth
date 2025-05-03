# These are used to restrict HCLG on the word side
vocab: text
	cat text | cut -f2- -d' ' | tr ' ' '\12' | sort -u | egrep '[A-Z]' | egrep -v '(FRICATIVE|VOCALIC)' > vocab

vocab.txt.fst: vocab
	cat vocab | awk '{printf("0 1 %s\n",$$0)} END {printf("1\n")}' > vocab.txt.fst

vocab0.fst:
	/projects/speech/ASR/kaldi/tools/openfst/bin/fstcompile --isymbols=../lang_nosp/words.txt --acceptor vocab.txt.fst vocab0.fst

vocab.fst: vocab0.fst
	/projects/speech/ASR/kaldi/tools/openfst/bin/fstclosure vocab0.fst vocab1.fst
	/projects/speech/ASR/kaldi/tools/openfst/bin/fstarcsort vocab1.fst vocab.fst
