cat data_clean/*/*/text | tr -d '\r' > data_clean/pooled_text
cat data_clean/*/*/truth | tr -d '\r' > data_clean/pooled_truth
