awk '{
  printf "%s", $0
  for (i=1; i<=length($0); i++) printf " %s", substr($0,i,1)
  printf "\n"
}' vocab.txt > lexicon.txt
